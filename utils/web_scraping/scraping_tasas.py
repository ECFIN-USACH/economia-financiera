# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 00:26:42 2025

@author: Lucas Salazar

    @TODO: Añadir funcion para interpolación para datos faltantes.
"""


import re
from typing import List, Tuple, Dict
import pandas as pd
import requests
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.interpolate import UnivariateSpline
import numpy as np


def fetch_interest_rate_data(url_template: str, year: int) -> pd.DataFrame:
    """
    Descarga y procesa los datos de tasas de interés desde el Banco Central para un año dado.

    Args:
        url_template (str): URL con un placeholder '{year}' para el año.
        year (int): Año a consultar.

    Returns:
        pd.DataFrame: DataFrame en formato largo con las columnas ['Serie', 'Fecha', 'Tasa'].
    """
    url = url_template.format(year=year)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data. Status code: {response.status_code}")

    # Se asume que la tabla está en la primera posición
    df = pd.read_html(response.content, header=0, thousands=".", decimal=",")[0]
    df.dropna(axis=1, how="all", inplace=True)

    # Convertir el DataFrame a formato largo (melt) para facilitar el pivot
    df_long = pd.melt(df, id_vars=["Serie"], var_name="Fecha", value_name="Tasa")

    # Traducción de nombres de meses de español a inglés para poder convertir a datetime
    month_translation = {
        "Ene": "Jan",
        "Feb": "Feb",
        "Mar": "Mar",
        "Abr": "Apr",
        "May": "May",
        "Jun": "Jun",
        "Jul": "Jul",
        "Ago": "Aug",
        "Sep": "Sep",
        "Oct": "Oct",
        "Nov": "Nov",
        "Dic": "Dec",
    }
    for esp, eng in month_translation.items():
        df_long["Fecha"] = df_long["Fecha"].str.replace(esp, eng, regex=True)

    df_long["Fecha"] = pd.to_datetime(
        df_long["Fecha"], format="%d.%b.%Y", errors="coerce", dayfirst=True
    )
    return df_long


def fetch_multiple_years(url_template: str, years: List[int]) -> pd.DataFrame:
    """
    Descarga y concatena los datos para una lista de años.

    Args:
        url_template (str): URL con placeholder '{year}'.
        years (List[int]): Lista de años a consultar.

    Returns:
        pd.DataFrame: DataFrame concatenado de todos los años.
    """
    df_list = []
    for y in years:
        df_year = fetch_interest_rate_data(url_template, y)
        df_list.append(df_year)
    return pd.concat(df_list, ignore_index=True)


# =============================================================================
# FUNCIONES DE RENOMBRADO Y EXTRACCIÓN DE VENCIMIENTOS
# =============================================================================


def extract_tenor(series_name: str) -> float:
    """
    Extrae el vencimiento de la serie en años.

    Si en el nombre se indica "días", se divide por 360.
    Si se indica "año" o "años", se toma el número tal cual.

    Args:
        series_name (str): Nombre original de la serie.

    Returns:
        float: Vencimiento en años.
    """
    m = re.search(r"(\d+)", series_name)
    if m:
        num = float(m.group(1))
        if "día" in series_name.lower():
            return num / 360.0
        elif "año" in series_name.lower():
            return num
        else:
            return num
    return np.nan


def rename_series(series_name: str, swap=True) -> str:
    """
    Genera un nuevo nombre abreviado para la serie.

    Si la serie es en pesos se utiliza el prefijo "SPCCLP" y si es en UF "SPCCLF".
    Se extrae el número de vencimiento para formar el nuevo nombre.

    Ejemplos:
        "SPC en pesos 90 días" -> "SPCCLP90"
        "SPC en UF 2 años" -> "SPCCLF2"

    Args:
        series_name (str): Nombre original de la serie.

    Returns:
        str: Nuevo nombre abreviado.
    """
    lower_name = series_name.lower()
    if swap:

        if "pesos" in lower_name:
            prefix = "SPCCLP"
        elif "uf" in lower_name:
            prefix = "SPCCLF"
        else:
            prefix = "SPCCL"

    else:
        if "pesos" in lower_name:
            prefix = "BCP_BTP"
        elif "uf" in lower_name:
            prefix = "BCU_BTU"
        else:
            prefix = "BCL"

    m = re.search(r"(\d+)", series_name)
    if m:
        return prefix + m.group(1)
    return series_name


def apply_renaming(
    df: pd.DataFrame, swap: bool
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Renombra las series y agrega una columna con el vencimiento (en años).

    Args:
        df (pd.DataFrame): DataFrame con columna 'Serie'.

    Returns:
        Tuple[pd.DataFrame, Dict[str, float]]: DataFrame con la columna 'Serie' renombrada
        y un diccionario mapeando el nuevo nombre a su vencimiento en años.
    """
    # Crear una copia para no alterar el original
    df = df.copy()
    # Se crea una columna con el vencimiento en años a partir del nombre original
    df["Tenor"] = df["Serie"].apply(extract_tenor)
    # Se renombra la serie
    df["Serie"] = df["Serie"].apply(rename_series, swap=swap)

    # Crear un diccionario: nombre de la serie (ya renombrado) -> tenor
    tenor_dict = df.groupby("Serie")["Tenor"].first().to_dict()
    return df, tenor_dict


# =============================================================================
# PIVOTE Y SEPARACIÓN DE INSTRUMENTOS
# =============================================================================


def pivot_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza un pivot del DataFrame para que cada columna corresponda a un instrumento
    y el índice a la fecha.

    Args:
        df (pd.DataFrame): DataFrame con columnas ['Serie', 'Fecha', 'Tasa'].

    Returns:
        pd.DataFrame: DataFrame pivotado.
    """
    pivot_df = df.pivot(index="Fecha", columns="Serie", values="Tasa")
    # Ordenar por fecha
    pivot_df.sort_index(inplace=True)
    return pivot_df


def separate_instruments(
    pivot_df: pd.DataFrame, swap: bool
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa las columnas del pivot en dos DataFrames: uno para instrumentos en pesos y otro en UF.

    Args:
        pivot_df (pd.DataFrame): DataFrame pivotado con columnas renombradas.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (df_pesos, df_uf)
    """
    if swap:
        df_pesos = pivot_df.filter(like="SPCCLP")
        df_pesos = df_pesos[
            [
                "SPCCLP90",
                "SPCCLP180",
                "SPCCLP360",
                "SPCCLP2",
                "SPCCLP3",
                "SPCCLP4",
                "SPCCLP5",
                "SPCCLP10",
            ]
        ]
        df_uf = pivot_df.filter(like="SPCCLF")
        df_uf = df_uf[
            [
                "SPCCLF1",
                "SPCCLF2",
                "SPCCLF3",
                "SPCCLF4",
                "SPCCLF5",
                "SPCCLF10",
                "SPCCLF20",
            ]
        ]
    else:
        df_pesos = pivot_df.filter(like="BCP")
        df_pesos = df_pesos[
            [
                "BCP_BTP1",
                "BCP_BTP2",
                "BCP_BTP5",
                "BCP_BTP10",
            ]
        ]
        df_uf = pivot_df.filter(like="BCU")
        df_uf = df_uf[
            [
                "BCU_BTU1",
                "BCU_BTU2",
                "BCU_BTU5",
                "BCU_BTU10",
                "BCU_BTU20",
                "BCU_BTU30",
            ]
        ]

    return df_pesos, df_uf


# =============================================================================
# FUNCIONES DE INTERPOLACIÓN E AJUSTE DE CURVA
# =============================================================================


def spline_interpolation(
    x: np.ndarray, y: np.ndarray, s: float = 0, k: int = 3
) -> UnivariateSpline:
    """
    Retorna una función spline que interpola (o suaviza) los datos.

    Args:
        x (np.ndarray): Valores de la variable independiente (por ejemplo, vencimientos).
        y (np.ndarray): Tasas observadas.
        s (float): Factor de suavizado (0 para interpolación exacta).
        k (int): Dimensión de spline (3 para spline cúbica)
    Returns:
        UnivariateSpline: Función spline interpoladora.
    """
    return UnivariateSpline(x, y, s=s, k=k)


def nelson_siegel_yield(
    maturities: np.ndarray, beta0: float, beta1: float, beta2: float, tau: float
) -> np.ndarray:
    """
    Modelo de Nelson-Siegel para calcular la curva de rendimiento.

    Args:
        maturities (np.ndarray): Vector de vencimientos (en años).
        beta0, beta1, beta2 (float): Parámetros de nivel, pendiente y curvatura.
        tau (float): Parámetro de decaimiento.

    Returns:
        np.ndarray: Tasas calculadas para cada vencimiento.
    """
    # Para evitar división por cero, se usa np.where
    factor = np.where(
        maturities == 0, 1, (1 - np.exp(-maturities / tau)) / (maturities / tau)
    )
    return beta0 + beta1 * factor + beta2 * (factor - np.exp(-maturities / tau))


def fit_nelson_siegel(
    maturities: np.ndarray, yields: np.ndarray
) -> Tuple[float, float, float, float]:
    """
    Ajusta el modelo de Nelson-Siegel a los datos observados mediante minimización de errores.

    Args:
        maturities (np.ndarray): Vectores de vencimientos.
        yields (np.ndarray): Tasas observadas.

    Returns:
        Tuple[float, float, float, float]: Parámetros ajustados (beta0, beta1, beta2, tau).
    """

    # Función objetivo: error cuadrático
    def objective(params):
        beta0, beta1, beta2, tau = params
        fitted = nelson_siegel_yield(maturities, beta0, beta1, beta2, tau)
        return np.sum((yields - fitted) ** 2)

    # Parámetros iniciales (se pueden ajustar)
    initial_params = [np.mean(yields), -1, 1, 1]
    bounds = [(-10, 10), (-10, 10), (-10, 10), (0.01, 10)]
    result = minimize(objective, initial_params, bounds=bounds)
    if result.success:
        return tuple(result.x)
    else:
        raise RuntimeError("Nelson-Siegel optimization failed")


# =============================================================================
# FUNCIONES DE GRAFICACIÓN
# =============================================================================


def plot_curve_for_date(
    pivot_df: pd.DataFrame, tenor_dict: Dict[str, float], date: pd.Timestamp, title: str
):
    """
    Para una fecha dada, grafica los valores observados, la interpolación spline
    y el ajuste Nelson-Siegel.

    Args:
        pivot_df (pd.DataFrame): DataFrame pivot con tasas.
        tenor_dict (Dict[str, float]): Diccionario con vencimientos de cada instrumento.
        date (pd.Timestamp): Fecha para la que se desea graficar.
        title (str): Título del gráfico.
    """
    if date not in pivot_df.index:
        raise ValueError("La fecha indicada no se encuentra en los datos")

    # Extraer los instrumentos disponibles en esa fecha (omitiendo NaN)
    data = pivot_df.loc[date].dropna()
    if data.empty:
        raise ValueError("No hay datos para la fecha indicada")

    # Obtener los vencimientos y tasas
    instrument_names = data.index.tolist()
    maturities = np.array([tenor_dict.get(inst, np.nan) for inst in instrument_names])
    tasas = data.values

    # Ordenar por vencimientos
    order = np.argsort(maturities)
    maturities = maturities[order]
    tasas = tasas[order]
    instrument_names = [instrument_names[i] for i in order]

    # Interpolación spline
    spline_func = spline_interpolation(maturities, tasas, s=0)
    x_new = np.linspace(maturities.min(), maturities.max(), 100)
    spline_y = spline_func(x_new)

    # Ajuste Nelson-Siegel
    try:
        beta0, beta1, beta2, tau = fit_nelson_siegel(maturities, tasas)
        ns_y = nelson_siegel_yield(x_new, beta0, beta1, beta2, tau)
    except Exception as e:
        print("Error en el ajuste Nelson-Siegel:", e)
        ns_y = np.full_like(x_new, np.nan)

    # Graficación
    plt.figure(figsize=(10, 6))
    plt.plot(maturities, tasas, "o", label="Observado")
    plt.plot(x_new, spline_y, "-", label="Spline Interpolación")
    plt.plot(x_new, ns_y, "--", label="Nelson-Siegel")
    plt.xlabel("Vencimiento (años)")
    plt.ylabel("Tasa (%)")
    plt.title(f"{title} - {date.strftime('%Y-%m-%d')}")
    plt.legend()
    plt.grid(True)
    plt.show()


def obtener_urls(swap: bool):
    if swap:
        URL_PESOS = (
            "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TASA_INTERES/MN_TASA_INTERES_09/"
            + "TI__TPM4/T31b?cbFechaDiaria={year}&cbFrecuencia=DAILY&cbCalculo=NONE&cbFechaBase="
        )
        URL_UF = (
            "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TASA_INTERES/MN_TASA_INTERES_09/"
            + "TI__TPM4_DIAS/638228603004699143?cbFechaDiaria={year}&cbFrecuencia=DAILY&cbCalculo"
            + "=NONE&cbFechaBase="
        )
    else:
        URL_PESOS = (
            "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TASA_INTERES/MN_TASA_INTERES_09/"
            + "TMS_15/T311?cbFechaDiaria={year}&cbFrecuencia=DAILY&cbCalculo=NONE&cbFechaBase="
        )
        URL_UF = (
            "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TASA_INTERES/MN_TASA_INTERES_09/"
            + "TMS_16/T312?cbFechaDiaria={year}&cbFrecuencia=DAILY&cbCalculo=NONE&cbFechaBase="
        )

    return URL_PESOS, URL_UF


# =============================================================================
# BLOQUE PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    swap = False
    URL_PESOS, URL_UF = obtener_urls(swap=swap)
    # Ejemplo de consulta para varios años
    years = [2024, 2025]  # por ejemplo

    # Descarga y concatenación de datos
    df_pesos_raw = fetch_multiple_years(URL_PESOS, years)
    df_uf_raw = fetch_multiple_years(URL_UF, years)

    # Unir ambos DataFrames
    df_total = pd.concat([df_pesos_raw, df_uf_raw], ignore_index=True)

    # Aplicar renombrado y extraer vencimientos
    df_total, tenor_dict = apply_renaming(df_total, swap=swap)

    # Generar pivot
    pivot_df = pivot_data(df_total)

    # Separar instrumentos en pesos y UF (según prefijo)
    df_pesos, df_uf = separate_instruments(pivot_df, swap=swap)

    # Elegir una fecha (por ejemplo, la primera fecha disponible de cada grupo)
    # Para pesos:
    if not df_pesos.empty:
        date = df_pesos.index[0]
        date = df_pesos.index[-2]
        date = pd.Timestamp("2024-12-13 00:00:00")
        TITLE = "Bonos del Banco Central y Tesorería en Pesos"
        pivot_df = df_pesos.copy()
        plot_curve_for_date(pivot_df, tenor_dict, date, title=TITLE)

    # Para UF:
    if not df_uf.empty:
        date = df_uf.index[0]
        date = pd.Timestamp("2024-12-27 00:00:00")
        TITLE = "Swap Cámara Promedio UF"
        plot_curve_for_date(df_uf, tenor_dict, date, title=TITLE)
