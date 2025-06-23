"""
Aplicaciones Swaps
Economía Financiera
USACH 2025

@Lucas Salazar
"""
import pandas as pd
import matplotlib.pyplot as plt

class DataCurves:
    def __init__(self, fecha_inicio:str = '2005-06-01', fecha_fin:str = '2015-06-01'):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        
    def get_bond_usa(self):
    
        excel_filename = "data/yield_curve_historical_usa.xlsx"
        df_bond_usa = pd.read_excel(excel_filename, index_col='date')
        
        df_bond_usa = self.filter_date(df_bond_usa)
        return df_bond_usa
    
    def get_swap_usa(self):
    
        excel_filename = "data/yield_swap_curve_historical_usa.xlsx"
        df_swap_usa = pd.read_excel(excel_filename, index_col='date')
        df_swap_usa = self.filter_date(df_swap_usa)
        
        return df_swap_usa
    
    def filter_date(self, df):
        df = df[self.fecha_inicio:self.fecha_fin]
        return df


self = DataCurves()

df_swap_usa = self.get_swap_usa()
df_bond_usa = self.get_bond_usa()

def compute_swap_spreads(
    df_swap: pd.DataFrame,
    df_bond: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula los swap spreads para las fechas y tenores comunes
    entre df_swap y df_bond.

    :param df_swap: DataFrame de tasas swap (índice: fechas, columnas: tenores)
    :param df_bond: DataFrame de yields de bonos (índice: fechas, columnas: tenores)
    :return: DataFrame de swap spreads (swap - yield) para tenores comunes
    """
    # 1) Intersectar fechas
    common_dates = df_swap.index.intersection(df_bond.index)
    if common_dates.empty:
        raise ValueError("No hay fechas comunes entre df_swap y df_bond.")

    # 2) Intersectar tenores (columnas)
    common_tenors = df_swap.columns.intersection(df_bond.columns)
    if common_tenors.empty:
        raise ValueError("No hay tenores comunes entre df_swap y df_bond.")

    # 3) Seleccionar sub-DataFrames con fechas y tenores comunes
    swap_common = df_swap.loc[common_dates, common_tenors]
    bond_common = df_bond.loc[common_dates, common_tenors]

    # 4) Calcular spread (swap - bond)
    spreads = swap_common.subtract(bond_common)

    return spreads

# === Uso de la función ===
spread_df = compute_swap_spreads(df_swap_usa, df_bond_usa)

spread_df = spread_df[['1 Año', '5 Años',  '10 Años', '30 Años']]

plt.figure(figsize=(12, 6))  # ancho=12", alto=6"
# === Gráfico de la evolución histórica ===
plt.figure()
for tenor in spread_df.columns:
    plt.plot(spread_df.index, spread_df[tenor], label=tenor)

plt.xlabel("Fecha")
plt.ylabel("Swap Spread (puntos porcentuales)")
plt.title("Evolución histórica de los Swap Spreads")
plt.legend()
plt.tight_layout()
plt.show()



#### Swap Spread Chile

import pandas as pd
from typing import List

def read_and_merge_curvas_spread(
    filepath: str = 'data/curvas_spread_chile.xlsx',
    sheet_names: List[str] = ['swap', 'bono']
) -> pd.DataFrame:
    """
    Lee las hojas indicadas de un archivo Excel y devuelve un único DataFrame
    con la unión por intersección (inner join) de las fechas.

    Parámetros
    ----------
    filepath : str
        Ruta al archivo Excel que contiene las hojas.
    sheet_names : List[str]
        Lista de nombres de hoja a leer (por defecto ['swap', 'bono']).

    Retorna
    -------
    pd.DataFrame
        DataFrame con todas las columnas de ambas hojas, pero solo las filas
        cuyas fechas aparecen en todas las hojas (intersección).
    """
    # 1. Leer cada hoja en un dict de DataFrames, usando la primera columna como índice de fechas
    dfs: dict[str, pd.DataFrame] = pd.read_excel(
        filepath,
        sheet_name=sheet_names,
        index_col=0,
        engine='openpyxl'
    )

    # 2. Concatenar horizontalmente, reteniendo solo la intersección de índices (join='inner')
    df_merged = pd.concat(dfs.values(), axis=1, join='outer')

    # 3. Ordenar ascendentemente por fecha
    df_merged.sort_index(inplace=True)

    return df_merged

def plot_swap_vs_bono(df_curves):
    """
    Por cada fecha en df_curves dibuja dos subplots:
      - Izquierda: Swap vs Bono en CLP (tenor en años)
      - Derecha: Swap vs Bono en UF (tenor en años)
    """
    # ticks comunes para cada subplot
    xticks_clp = sorted(set(TENOR_SWAP_CLP + TENOR_BONO_CLP))
    xticks_uf  = sorted(set(TENOR_SWAP_UF + TENOR_BONO_UF))

    for fecha, row in df_curves.iterrows():
        fig, (ax_clp, ax_uf) = plt.subplots(1, 2, figsize=(12, 4))

        # CLP
        ax_clp.plot(TENOR_SWAP_CLP,    row[SWAP_CLP],  marker='o', label='Swap CLP')
        ax_clp.plot(TENOR_BONO_CLP,    row[BONO_CLP],  marker='s', label='Bono CLP')
        ax_clp.set_xticks(xticks_clp)
        ax_clp.set_xticklabels([f"{t:g}" for t in xticks_clp])
        ax_clp.set_title(f'CLP – {fecha.date()}')
        ax_clp.set_xlabel('Tenor (años)')
        ax_clp.legend()
        ax_clp.grid(True, linestyle='--', alpha=0.5)

        # UF
        ax_uf.plot(TENOR_SWAP_UF,      row[SWAP_UF],   marker='o', label='Swap UF')
        ax_uf.plot(TENOR_BONO_UF,      row[BONO_UF],   marker='s', label='Bono UF')
        ax_uf.set_xticks(xticks_uf)
        ax_uf.set_xticklabels([f"{t:g}" for t in xticks_uf])
        ax_uf.set_title(f'UF – {fecha.date()}')
        ax_uf.set_xlabel('Tenor (años)')
        ax_uf.legend()
        ax_uf.grid(True, linestyle='--', alpha=0.5)

        plt.suptitle(f'Curvas Swap vs Bonos – {fecha.date()}', y=1.02)
        plt.tight_layout()
        plt.show()



# Ejemplo de uso:
df_curves = read_and_merge_curvas_spread('data/curvas_spread_chile.xlsx')
print(df_curves.head())

df_curves = df_curves['2005-01-01':'2008-01-01']


# constantes con el orden de columnas
SWAP_CLP =   ['SPCCLP90',  'SPCCLP180',  'SPCCLP360', 'SPCCLP2',
              'SPCCLP3',   'SPCCLP4',    'SPCCLP5',   'SPCCLP10']
TENOR_SWAP_CLP = [90/360,       180/360,      360/360,    2,
                  3,            4,            5,          10]

SWAP_UF =    ['SPCCLF1',   'SPCCLF2',   'SPCCLF3',
              'SPCCLF4',   'SPCCLF5',   'SPCCLF10',  'SPCCLF20']
TENOR_SWAP_UF = [1,           2,           3,
                 4,           5,           10,         20]

BONO_CLP =   ['BCP_BTP1',  'BCP_BTP2',  'BCP_BTP5',  'BCP_BTP10']
TENOR_BONO_CLP = [1,         2,           5,           10]

BONO_UF =    ['BCU_BTU1',  'BCU_BTU2',  'BCU_BTU5',
              'BCU_BTU10', 'BCU_BTU20', 'BCU_BTU30']
TENOR_BONO_UF = [1,         2,           5,
                 10,        20,          30]


plot_swap_vs_bono(df_curves)

df_data = df_curves['2006-06-21':'2006-06-23']

df_data['SPCCLF2']

df_data['BCU_BTU2']

df_data['SPCCLF2'] - df_data['BCU_BTU2']




df_data['SPCCLF5']

df_data['BCU_BTU5']

df_data['SPCCLF5'] - df_data['BCU_BTU5']


#### Graficar curvas historicas

# constantes con las columnas de 5 años
SWAP_5Y = 'SPCCLP5'
BONO_5Y = 'BCP_BTP5'
# SWAP_5Y = 'SPCCLF5'
# BONO_5Y = 'BCU_BTU5'

def plot_5y_clp_swap_vs_bono(df_curves: pd.DataFrame) -> None:
    """
    Grafica la serie temporal de las tasas a 5 años para:
      - Swap en CLP (SPCCLP5)
      - Bono en CLP (BCP_BTP5)

    Parámetros
    ----------
    df_curves : pd.DataFrame
        DataFrame con índice de fechas y columnas que incluyen
        'SPCCLP5' y 'BCP_BTP5'.

    Comportamiento
    -------------
    Crea un gráfico de línea donde el eje x es la fecha y el y
    son las tasas a 5 años de swap y bono en CLP, etiquetadas y con
    leyenda.
    """
    # Extraer las dos series
    swap_5y = df_curves[SWAP_5Y]
    bono_5y = df_curves[BONO_5Y]

    # Crear la figura
    plt.figure(figsize=(10, 5))
    plt.plot(df_curves.index, swap_5y, marker='o', label='Swap CLP 5 años')
    plt.plot(df_curves.index, bono_5y, marker='s', label='Bono CLP 5 años')

    # Formato del gráfico
    plt.title('Tasas a 5 años: Swap CLF vs Bono BTU')
    plt.xlabel('Fecha')
    plt.ylabel('Tasa anual (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# Ejemplo de uso:
plot_5y_clp_swap_vs_bono(df_curves)

#### Aplicación Excel


##### Caso CLP

df_data = df_curves['2005-01-01':'2007-01-01']

df_data['Spread_2_CLP'] = df_data['SPCCLP2'] - df_data['BCP_BTP2']

df_data['Spread_5_CLP'] = df_data['SPCCLP5'] - df_data['BCP_BTP5']


# Suponiendo que df_data ya está definido en el entorno
plt.figure(figsize=(10, 6))
plt.plot(df_data.index, df_data['Spread_2_CLP'], marker='o', label='Spread 2 años')
plt.plot(df_data.index, df_data['Spread_5_CLP'], marker='s', label='Spread 5 años')

plt.title('Spreads a 2 y 5 años')
plt.xlabel('Fecha')
plt.ylabel('Spread (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# Supongamos que df_data ya está cargado en el entorno con las columnas 'Spread_2' y 'Spread_5'.
# Ajusta el tamaño de la ventana de la media móvil si lo deseas.
window = 12  # media móvil de 12 períodos

# Cálculo de la media móvil
ma2 = df_data['Spread_2'].rolling(window=window).mean()
ma5 = df_data['Spread_5'].rolling(window=window).mean()

# Gráfico de la media móvil
plt.figure(figsize=(10, 6))
plt.plot(ma2.index, ma2, marker='o', label=f'Media móvil {window} períodos - Spread 2 años')
plt.plot(ma5.index, ma5, marker='s', label=f'Media móvil {window} períodos - Spread 5 años')

plt.title('Media móvil de Spreads a 2 y 5 años')
plt.xlabel('Fecha')
plt.ylabel('Spread (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


##### Caso UF


df_data = df_curves['2005-01-01':'2007-01-01']

df_data['Spread_2_UF'] = df_data['SPCCLF2'] - df_data['BCU_BTU2']

df_data['Spread_5_UF'] = df_data['SPCCLF5'] - df_data['BCU_BTU5']


# Suponiendo que df_data ya está definido en el entorno
plt.figure(figsize=(10, 6))
plt.plot(df_data.index, df_data['Spread_2_UF'], marker='o', label='Spread 2 años')
plt.plot(df_data.index, df_data['Spread_5_UF'], marker='s', label='Spread 5 años')

plt.title('Spreads a 2 y 5 años')
plt.xlabel('Fecha')
plt.ylabel('Spread (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# Supongamos que df_data ya está cargado en el entorno con las columnas 'Spread_2' y 'Spread_5'.
# Ajusta el tamaño de la ventana de la media móvil si lo deseas.
window = 12  # media móvil de 12 períodos

# Cálculo de la media móvil
ma2 = df_data['Spread_2_UF'].rolling(window=window).mean()
ma5 = df_data['Spread_5_UF'].rolling(window=window).mean()

# Gráfico de la media móvil
plt.figure(figsize=(10, 6))
plt.plot(ma2.index, ma2, marker='o', label=f'Media móvil {window} períodos - Spread 2 años')
plt.plot(ma5.index, ma5, marker='s', label=f'Media móvil {window} períodos - Spread 5 años')

plt.title('Media móvil de Spreads a 2 y 5 años')
plt.xlabel('Fecha')
plt.ylabel('Spread (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
