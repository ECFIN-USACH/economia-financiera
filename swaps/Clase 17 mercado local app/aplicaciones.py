


import numpy as np
import pandas as pd


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

import pandas as pd
import matplotlib.pyplot as plt
from typing import List

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
