# Reporte de Clase 06

## Objetivos  
- **Comprender el manejo de riesgo de tasas:** Presentar los fundamentos del riesgo de tasa de interés y la forma en que se puede cuantificar y gestionar utilizando medidas como la duración y la convexidad.  
- **Analizar estrategias de spread y convergencia:** Revisar cómo comparar bonos de diferentes vencimientos para identificar oportunidades de arbitraje o convergencia, basándose en diferencias de tasas.  
- **Aplicación práctica con Python:** Implementar un caso práctico en Jupyter Notebook en el que se descarguen datos reales de bonos del Tesoro desde el FRED, se calculen medidas de riesgo y se determine el mark-to-market diario utilizando fórmulas de duración y convexidad.  
- **Visualizar la curva de bonos:** Graficar la evolución y la estructura de la curva de rendimientos en distintos plazos, enfatizando la dinámica de convergencia entre estos.

## Contenido  
Se parte de la introducción al riesgo de tasas explicando que la sensibilidad del precio de un bono ante cambios en la tasa se mide a través de:  

- **Duración (D):** Que indica la variación porcentual en el precio ante un cambio unitario en la tasa.  
- **Convexidad (C):** Que permite ajustar la aproximación lineal para capturar la curvatura real en la relación precio-tasa.  

La variación en el precio de un bono se puede aproximar con la fórmula:  

\[
\Delta P \approx - D \cdot P \cdot \Delta y + \frac{1}{2} \cdot C \cdot P \cdot (\Delta y)^2
\]

donde:  
- \( P \) es el precio del bono  
- \( \Delta y \) es la variación en la tasa de interés  
- \( D \) es la duración  
- \( C \) es la convexidad  

Además, se introduce el cómputo de la diferencia de fechas en frecuencia anual utilizando una convención (por ejemplo, 360 o 365 días), lo que permite calcular adecuadamente los cambios diarios en un marco temporal anualizado.

Por otro lado, se analiza la estrategia de **spread o convergencia de tasas**. Esta estrategia consiste en comparar bonos de similar calidad crediticia pero de distintos vencimientos. La idea es aprovechar que, en condiciones de mercado, la estructura de plazos tiende a converger o presentar variaciones predecibles que pueden generar oportunidades de arbitraje.

## Metodología  
La clase se desarrollará en dos partes:

1. **Teoría y Fórmulas:**  
   Se expondrán los fundamentos teóricos sobre duración, convexidad y el manejo del riesgo de tasa, con énfasis en su aplicación para la evaluación de estrategias de spread y convergencia entre bonos. Se presentarán ejemplos con fórmulas detalladas, explicando cada variable y la lógica detrás de la valoración de bonos.

2. **Caso Práctico en Python:**  
   En un entorno Jupyter Notebook se utilizará un script en Python que realiza lo siguiente:  
   - **Obtención de datos:** Se importan los datos históricos de bonos del Tesoro desde FRED mediante un módulo de web scraping ubicado en el repositorio [ECFIN-USACH/economia-financiera](https://github.com/ECFIN-USACH/economia-financiera/blob/main/utils/web_scraping/fred_interest_rates.py).  
   - **Cálculo del Mark-to-Market Diario:** Se calcula la variación diaria en el precio utilizando la aproximación basada en duración y convexidad, ajustando por la convención anual (por ejemplo, 360 o 365 días) en el cómputo de la diferencia de fechas.  
   - **Visualización:** Se generan gráficos para visualizar la evolución de la curva de rendimientos a distintos plazos, facilitando el análisis de convergencia de tasas.

## Observaciones  
- Se recomienda revisar detalladamente cada parte del código y entender la interpretación económica de la duración y convexidad.  
- La precisión en el cálculo del mark-to-market es fundamental, por lo cual se enfatiza en el correcto manejo de la diferencia de fechas mediante una convención de días.  
- Los ejemplos presentados se sustentan en datos reales del FRED, lo cual añade una dimensión práctica y actualizada a la clase.  
- Se sugiere al alumno comparar los resultados obtenidos con la teoría y realizar análisis de sensibilidad para distintos supuestos de duración, convexidad y convención de días.

---

# Ejemplo Práctico en Python  
A continuación, se presenta un ejemplo de código en formato Markdown adecuado para un Jupyter Notebook. Este ejemplo ilustra el proceso de descarga de datos, cálculo del mark-to-market diario y la visualización de la curva de bonos.

```python
# %% [markdown]
"""
# Estrategias con Bonos: Spread y Convergencia de Tasas
En este ejemplo, aplicaremos técnicas de manejo de riesgo de tasas utilizando las medidas de duración y convexidad para calcular el mark-to-market diario de bonos del Tesoro. Utilizaremos datos reales descargados desde FRED mediante un módulo de web scraping.
"""

# %% Código

# Importar librerías necesarias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Importar función para obtener datos de bonos del Tesoro desde FRED.
# Se asume que la función get_treasury_data extrae series de tiempo para distintos vencimientos.
try:
    from utils.web_scraping.fred_interest_rates import get_treasury_data
except ImportError:
    # Para efectos demostrativos, se simularán datos de ejemplo si no se encuentra el módulo.
    def get_treasury_data(maturity='10Y'):
        # Simulación de datos: generar una serie diaria de rendimientos ficticios
        dates = pd.date_range(start='2023-01-01', periods=200, freq='B')
        np.random.seed(42)
        rates = np.cumsum(np.random.randn(len(dates)) * 0.005) + 0.03  # rendimientos alrededor de 3%
        return pd.Series(rates, index=dates, name=f'Treasury_{maturity}')
        
# Parámetros de ejemplo
bond_price = 100  # Precio nominal del bono
duration = 7.0    # Duración en años (valor de ejemplo)
convexity = 50.0  # Convexidad (valor de ejemplo)
convention = 360  # Convención en días para cómputo de frecuencia anual

# Descargar datos para distintos vencimientos
maturities = ['2Y', '5Y', '10Y']
data = {}
for mat in maturities:
    data[mat] = get_treasury_data(maturity=mat)

# Crear un DataFrame único
df_rates = pd.DataFrame(data)
df_rates = df_rates.sort_index()

# Visualizar la serie de rendimientos
plt.figure(figsize=(10, 6))
for mat in maturities:
    plt.plot(df_rates.index, df_rates[mat], label=f'{mat} Rendimiento')
plt.title('Evolución del Rendimiento de Bonos del Tesoro')
plt.xlabel('Fecha')
plt.ylabel('Rendimiento (%)')
plt.legend()
plt.grid(True)
plt.show()

# Calcular el mark-to-market diario utilizando la aproximación de duración y convexidad.
# Se calculará la variación de precio diaria para cada bono.
def calculate_mtm(prices, duration, convexity, convention=360):
    """
    Calcula la variación en precio (mark-to-market) de un bono dada la duración, convexidad y un cambio en la tasa.
    
    Parámetros:
    - prices: Serie de tasas o rendimientos (en decimal) para el bono.
    - duration: Duración del bono (en años).
    - convexity: Convexidad del bono.
    - convention: Número de días en el año según la convención elegida.
    
    Retorna:
    - DataFrame con la variación diaria en el precio (MTM).
    """
    # Diferencia de tasas diaria
    delta_y = prices.diff()
    
    # Diferencia de fechas en días y factor de tiempo (se asume que el índice es datetime)
    dt = prices.index.to_series().diff().dt.days / convention
    
    # Se elimina el primer registro (NaN) en los cálculos
    dt = dt.fillna(0)
    delta_y = delta_y.fillna(0)
    
    # Aproximación del cambio de precio por cada día
    # ΔP = -duration * P * Δy + 0.5 * convexity * P * (Δy)^2
    dP = - duration * bond_price * delta_y + 0.5 * convexity * bond_price * (delta_y)**2
    # Ajustamos por el factor tiempo dt (en años)
    dP_adjusted = dP * dt
    
    return dP_adjusted

# Aplicar el cálculo para cada serie de bonos
mtm_results = {}
for mat in maturities:
    mtm_results[mat] = calculate_mtm(df_rates[mat], duration, convexity, convention)

df_mtm = pd.DataFrame(mtm_results, index=df_rates.index)

# Visualizar el mark-to-market diario
plt.figure(figsize=(10, 6))
for mat in maturities:
    plt.plot(df_mtm.index, df_mtm[mat], label=f'{mat} MTM')
plt.title('Mark-to-Market Diario para Bonos del Tesoro')
plt.xlabel('Fecha')
plt.ylabel('Cambio en Precio')
plt.legend()
plt.grid(True)
plt.show()

# Graficar la curva de bonos al final del período analizado
final_date = df_rates.index[-1]
final_rates = df_rates.loc[final_date]
maturities_numeric = [float(mat[:-1]) for mat in maturities]  # Convertir "2Y", "5Y", etc. a numérico

plt.figure(figsize=(8, 5))
plt.plot(maturities_numeric, final_rates.values * 100, marker='o')
plt.title(f'Curva de Rendimientos - {final_date.date()}')
plt.xlabel('Plazo (años)')
plt.ylabel('Rendimiento (%)')
plt.grid(True)
plt.show()

# %% [markdown]
"""
## Conclusiones y Consideraciones
- **Duración y Convexidad:** Permiten estimar cómo responderá el precio del bono ante variaciones en las tasas, siendo esenciales para la gestión del riesgo de tasa.
- **Cómputo de Fechas:** El uso de una convención (360 o 365) es clave para ajustar la escala temporal de las variaciones diarias.
- **Estrategias de Spread y Convergencia:** Al comparar bonos de distintos plazos, se pueden identificar oportunidades basadas en la convergencia o divergencia de sus rendimientos.
- **Visualización:** Los gráficos ayudan a entender tanto la evolución histórica de los rendimientos como la estructura de plazos en la fecha analizada.

Este ejemplo puede ampliarse o ajustarse considerando diferentes supuestos de duración y convexidad, o integrando modelos más sofisticados para la predicción de tasas.
"""
```
