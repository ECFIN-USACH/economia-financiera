import os
import requests
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv
from loguru import logger

# Cargar variables de entorno
load_dotenv()


def load_api_key() -> str:
    """Obtiene la API key de las variables de entorno."""
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        logger.error("No se encontró la API key en las variables de entorno.")
        raise ValueError("API key no encontrada.")
    logger.info("API key cargada correctamente.")
    return api_key


def fetch_series_data(series_id: str, series_label: str, api_key: str) -> pd.DataFrame:
    """
    Consulta a la API de FRED y retorna el DataFrame histórico para un instrumento.

    Args:
        series_id: Identificador de la serie.
        series_label: Etiqueta legible (ej. '1 Mes').
        api_key: Clave de la API.

    Returns:
        DataFrame con columnas 'date' y la serie renombrada con series_label.
    """
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    logger.info("Consultando datos para '{}' ({})", series_label, series_id)
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(
            "Error al consultar {}. Código: {}", series_label, response.status_code
        )
        raise Exception(f"Error en la consulta de {series_label}")
    data = response.json()
    df = pd.DataFrame(data.get("observations", []))
    if df.empty:
        logger.warning("No se encontraron datos para '{}'", series_label)
        return pd.DataFrame()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df[["date", "value"]].dropna().sort_values("date")
    # Renombramos la columna 'value' para identificar el instrumento
    df.rename(columns={"value": series_label}, inplace=True)
    logger.info("Datos para '{}' obtenidos ({} registros)", series_label, len(df))
    return df


def fetch_all_series(series_ids: dict, api_key: str) -> dict:
    """
    Consulta todas las series indicadas y retorna un diccionario con el DataFrame histórico de cada instrumento.

    Args:
        series_ids: Diccionario con {Etiqueta: id_serie}.
        api_key: Clave de la API.

    Returns:
        Diccionario {Etiqueta: DataFrame}.
    """
    series_data = {}
    for label, series_id in series_ids.items():
        try:
            df = fetch_series_data(series_id, label, api_key)
            if not df.empty:
                series_data[label] = df
        except Exception as e:
            logger.error("Error al obtener datos para '{}': {}", label, e)
    return series_data


def combine_historical_data(series_data: dict) -> pd.DataFrame:
    """
    Combina los datos históricos de todos los instrumentos en un único DataFrame.
    El DataFrame resultante tendrá como índice las fechas y como columnas las etiquetas (plazos).

    Args:
        series_data: Diccionario {Etiqueta: DataFrame}.

    Returns:
        DataFrame combinado con unión externa sobre la fecha.
    """
    logger.info("Combinando datos históricos de todas las series.")
    combined_df = None
    for label, df in series_data.items():
        df = df.set_index("date")
        if combined_df is None:
            combined_df = df
        else:
            combined_df = combined_df.join(df, how="outer")
    combined_df.sort_index(inplace=True)
    logger.info(
        "Datos combinados: {} fechas, {} series.",
        len(combined_df),
        combined_df.shape[1],
    )
    return combined_df


def get_latest_yield_curve(series_data: dict) -> (pd.DataFrame, str):
    """
    Extrae el último valor (más reciente) de cada instrumento y construye la curva de rendimiento.

    Returns:
        - DataFrame con columnas 'Plazo' y 'Rendimiento'
        - Fecha (string) común del último registro.
    """
    latest_values = {}
    latest_dates = []
    for label, df in series_data.items():
        if df.empty:
            continue
        latest_record = df.iloc[-1]
        latest_values[label] = latest_record[label]
        latest_dates.append(latest_record["date"])
    if not latest_dates:
        logger.error("No se encontraron fechas en los datos.")
        raise Exception("No hay datos para extraer la curva.")
    # Suponiendo que todas las series están actualizadas en la misma fecha
    common_date = max(latest_dates).strftime("%Y-%m-%d")
    latest_df = pd.DataFrame(
        {
            "Plazo": list(latest_values.keys()),
            "Rendimiento": list(latest_values.values()),
        }
    )
    logger.info("Curva de rendimiento extraída para la fecha: {}", common_date)
    return latest_df, common_date


def get_latest_yield_curve_from_df(df: pd.DataFrame) -> (pd.DataFrame, str):
    """
    Extrae la curva de rendimiento más reciente a partir de un DataFrame
    en el que el índice es la fecha (datetime) y cada columna corresponde a un instrumento.

    Returns:
        - DataFrame con columnas 'Plazo' y 'Rendimiento'
        - Fecha (string) del registro más reciente.
    """
    if df.empty:
        logger.error("El DataFrame está vacío.")
        raise Exception("No hay datos para extraer la curva.")

    # Suponiendo que el DataFrame está ordenado cronológicamente por el índice (fecha)
    latest_date = df.index[-1]
    latest_row = df.loc[latest_date]

    # Convertir la serie (donde el índice son los plazos y los valores los rendimientos)
    # a un DataFrame con columnas 'Plazo' y 'Rendimiento'
    latest_df = latest_row.reset_index()
    latest_df.columns = ["Plazo", "Rendimiento"]

    common_date = latest_date.strftime("%Y-%m-%d")
    logger.info("Curva de rendimiento extraída para la fecha: {}", common_date)

    return latest_df, common_date


def save_historical_data_to_excel(hist_df: pd.DataFrame, filename: str) -> None:
    """
    Guarda el DataFrame histórico en un archivo Excel.

    Args:
        hist_df: DataFrame histórico combinado.
        filename: Nombre del archivo Excel de destino.
    """
    try:
        hist_df.to_excel(filename)
        logger.info("Datos históricos guardados en '{}'", filename)
    except Exception as e:
        logger.error("Error al guardar el archivo Excel: {}", e)
        raise


def plot_yield_curve_static(latest_df: pd.DataFrame, date_str: str) -> None:
    """
    Genera un gráfico estático de la curva de rendimientos usando Plotly.

    Args:
        latest_df: DataFrame con la curva del día más actual.
        date_str: Fecha a mostrar en el título del gráfico.
    """
    title = f"Curva de Rendimientos del Tesoro de EE.UU. - Fecha: {date_str}"
    fig = go.Figure(
        data=go.Scatter(
            x=latest_df["Plazo"],
            y=latest_df["Rendimiento"],
            mode="lines+markers",
            marker=dict(size=8),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Plazo",
        yaxis_title="Rendimiento (%)",
        hovermode="x",
    )
    fig.show()
    logger.info("Gráfico estático generado para la fecha {}", date_str)


def plot_yield_curve_animation(
    hist_df: pd.DataFrame, start_date: str, end_date: str
) -> None:
    """
    Crea un gráfico animado de la evolución de la yield curve en un intervalo de fechas.
    Se utiliza un slider y un botón 'Play' para recorrer los distintos días.

    Args:
        hist_df: DataFrame histórico (índice = fecha, columnas = plazos).
        start_date: Fecha de inicio (ej. '2024-01-01').
        end_date: Fecha final (ej. '2025-03-01').
    """
    # Filtrar por el rango de fechas
    mask = (hist_df.index >= pd.to_datetime(start_date)) & (
        hist_df.index <= pd.to_datetime(end_date)
    )
    filtered_df = hist_df.loc[mask]
    if filtered_df.empty:
        logger.error("No hay datos entre {} y {}", start_date, end_date)
        raise Exception("No hay datos en el rango de fechas especificado.")

    # Preparar los frames para la animación
    frames = []
    x_values = list(filtered_df.columns)  # Los plazos son las columnas
    for date, row in filtered_df.iterrows():
        frame = go.Frame(
            data=[
                go.Scatter(
                    x=x_values,
                    y=[row[col] for col in x_values],
                    mode="lines+markers",
                    marker=dict(size=8),
                )
            ],
            name=date.strftime("%Y-%m-%d"),
            layout=go.Layout(
                title_text=f"Curva de Rendimientos - {date.strftime('%Y-%m-%d')}"
            ),
        )
        frames.append(frame)

    # Configurar la figura inicial con la primera fecha del rango
    initial_date = filtered_df.index[0].strftime("%Y-%m-%d")
    initial_row = filtered_df.iloc[0]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_values,
                y=[initial_row[col] for col in x_values],
                mode="lines+markers",
                marker=dict(size=8),
            )
        ],
        layout=go.Layout(
            title=f"Curva de Rendimientos - {initial_date}",
            xaxis_title="Plazo",
            yaxis_title="Rendimiento (%)",
            hovermode="x",
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        {
                            "label": "Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 500, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 300},
                                },
                            ],
                        }
                    ],
                )
            ],
        ),
        frames=frames,
    )

    # Slider para seleccionar fechas específicas
    sliders = [
        {
            "currentvalue": {"prefix": "Fecha: "},
            "steps": [
                {
                    "label": date.strftime("%Y-%m-%d"),
                    "method": "animate",
                    "args": [
                        [date.strftime("%Y-%m-%d")],
                        {
                            "frame": {"duration": 500, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                }
                for date in filtered_df.index
            ],
        }
    ]
    fig.update_layout(sliders=sliders)
    fig.show()
    logger.info("Gráfico animado generado para el rango {} a {}", start_date, end_date)


def main():
    # Definición de las series a consultar
    series_ids_clp = {
        "1 Mes": "CH1MO",
        "3 Meses": "CH3MO",
        "6 Meses": "CH6MO",
        "1 Año": "CH1Y",
        "2 Años": "CH2Y",
        "3 Años": "CH3Y",
        "5 Años": "CH5Y",
        "7 Años": "CH7Y",
        "10 Años": "CH10Y",
    }
    series_ids = {
        "1 Mes": "DGS1MO",
        "3 Meses": "DGS3MO",
        "6 Meses": "DGS6MO",
        "1 Año": "DGS1",
        "2 Años": "DGS2",
        "3 Años": "DGS3",
        "5 Años": "DGS5",
        "7 Años": "DGS7",
        "10 Años": "DGS10",
        "20 Años": "DGS20",
        "30 Años": "DGS30",
    }

    api_key = load_api_key()

    # Obtener datos históricos para cada instrumento
    series_data = fetch_all_series(series_ids, api_key)

    # Combinar datos históricos y guardar en Excel
    hist_df = combine_historical_data(series_data)
    excel_filename = "yield_curve_historical_usa.xlsx"
    save_historical_data_to_excel(hist_df, excel_filename)

    # Extraer la curva del día más reciente y graficarla de forma estática
    latest_df, common_date = get_latest_yield_curve(series_data)
    plot_yield_curve_static(latest_df, common_date)

    # Crear un gráfico animado/interactivo para un intervalo de fechas
    # Ejemplo: desde '2024-01-01' hasta '2025-03-01'
    plot_yield_curve_animation(hist_df, "2024-01-01", "2025-03-01")


if __name__ == "__main__":
    main()
