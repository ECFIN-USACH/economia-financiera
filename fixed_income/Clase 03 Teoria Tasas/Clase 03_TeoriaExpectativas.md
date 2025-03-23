# Tasas Forward y Teoría de Expectativas: Un Análisis Integral

## 1. Repaso de Tasas Forward

### Fundamentos y Definición

Una **tasa forward** representa el tipo de interés implícito entre dos fechas futuras derivado de la estructura actual de tasas spot. Esencialmente, es el rendimiento de una inversión que comienza en una fecha futura y termina en otra fecha posterior.

Para una tasa forward que comienza en el tiempo $t$ y finaliza en $T$, usamos la notación:
$$f(t,T)$$

### Cálculo de Tasas Forward

El cálculo se basa en el principio de no arbitraje: dos estrategias que generan el mismo resultado final deben tener el mismo costo inicial.

**Fórmula general:**
$$
(1 + r_{0,T})^T = (1 + r_{0,t})^t \times (1 + f_{t,T})^{T-t}
$$

Despejando $f_{t,T}$:
$$
f_{t,T} = \left(\frac{(1 + r_{0,T})^T}{(1 + r_{0,t})^t}\right)^{\frac{1}{T-t}} - 1
$$

Donde:
- $r_{0,t}$ = Tasa spot desde hoy hasta el tiempo $t$
- $r_{0,T}$ = Tasa spot desde hoy hasta el tiempo $T$
- $f_{t,T}$ = Tasa forward desde $t$ hasta $T$

### Importancia en el Mercado

Las tasas forward son cruciales para:
- Valorar instrumentos de renta fija
- Formular expectativas económicas
- Identificar oportunidades de arbitraje temporal
- Diseñar estrategias de inversión y cobertura

## 2. Teoría de Expectativas y Estructura Temporal

### 2.1. Contexto y Fundamentos Teóricos

El análisis de la estructura temporal de las tasas de interés se fundamenta en el principio de no arbitraje y en la relación matemática entre los rendimientos spot y las tasas forward. Bajo condiciones de mercados eficientes y supuestos de agentes racionales, la tasa forward \( f(t,T) \) se relaciona con los tipos spot mediante la ecuación:

\[
(1 + r_{0,T})^T = (1 + r_{0,t})^t \times (1 + f_{t,T})^{T-t}
\]

Esta igualdad garantiza que no existan oportunidades de ganancia sin riesgo entre estrategias de inversión de diferente horizonte. Sin embargo, la interpretación económica de \( f(t,T) \) varía según el enfoque teórico que se adopte.

---

### 2.2. Teoría de las Expectativas Puras

#### Supuestos y Formulación Matemática

La **teoría de las expectativas puras** sostiene que la curva de rendimientos refleja exclusivamente las expectativas de tasas futuras. Bajo este paradigma, se parte de la siguiente hipótesis:

\[
f(t,T) = E[r(t,T)]
\]

donde \( E[r(t,T)] \) es la expectativa racional del tipo de interés que se observará en el futuro entre \( t \) y \( T \).

*Supuestos clave:*
- **Agentes risk neutral:** No se requiere compensación por asumir riesgo.
- **Mercados eficientes:** Toda la información disponible se incorpora en los precios actuales.
- **Expectativas racionales:** Los agentes forman expectativas que, en promedio, se ajustan a la realidad.

#### Limitaciones y Evidencia Empírica

Aunque la formulación es elegante y sencilla, numerosos estudios han encontrado que los forward rates tienden a predecir tasas futuras de manera sesgada. Esto se debe a la omisión de primas de riesgo y a la aversión al riesgo presente en la práctica. En otras palabras, si se observa una diferencia sistemática entre \( f(t,T) \) y la tasa spot observada posteriormente, se puede inferir la existencia de factores de compensación (riesgo, liquidez, etc.) que no son capturados en este modelo.

---

### 2.3. Teoría de la Liquidez (o de la Prima de Riesgo)

#### Incorporación del Term Premium

La **teoría de la liquidez** extiende el enfoque anterior al incorporar una prima de riesgo o “liquidez” que aumenta con el plazo. Se plantea que los inversores exigen un premio adicional para compensar la incertidumbre y la menor liquidez de los activos a largo plazo. La relación se expresa como:

\[
f(t,T) = E[r(t,T)] + \lambda_{t,T}
\]

donde \( \lambda_{t,T} \) es la prima de riesgo que generalmente crece con \( T-t \).

*Aspectos a destacar:*
- **No linealidad:** La prima no necesariamente crece de forma lineal, ya que depende de las condiciones del mercado, la aversión al riesgo y la percepción de liquidez.
- **Implicaciones empíricas:** Diversos estudios empíricos (por ejemplo, investigaciones basadas en modelos de tasa de interés afín) han encontrado evidencia de la existencia de primas de riesgo significativas, lo que explica por qué la curva de rendimiento suele ser ascendente aun cuando se esperan tasas futuras más bajas.

#### Interpretación en Términos de Política Monetaria

En un entorno donde la política monetaria es expansiva, la percepción de riesgo de los inversores puede aumentar, lo que a su vez incrementa \( \lambda_{t,T} \) y provoca un desplazamiento de la curva hacia arriba, sin que necesariamente se espere un incremento en las tasas futuras.

---

### 2.4. Teoría del Hábitat Preferido

#### Preferencias y Desviaciones de Portafolio

La **teoría del hábitat preferido** parte de la premisa de que los inversores tienen preferencias por ciertos horizontes temporales —su “hábitat”— y sólo se desplazarán a otros plazos si se les ofrece una compensación en forma de una prima de riesgo. Matemáticamente, se puede expresar de manera simplificada como:

\[
f(t,T) = E[r(t,T)] + \pi_{t,T}
\]

donde \( \pi_{t,T} \) representa la prima de riesgo asociada a la desviación del hábitat preferido. A diferencia de la teoría de liquidez, esta prima:
- **No es necesariamente creciente:** Dependiendo de las presiones de oferta y demanda en cada segmento del mercado, puede comportarse de manera no monotónica.
- **Refleja desequilibrios institucionales:** Por ejemplo, si un grupo importante de inversores prefiere activos a corto plazo, la demanda en el segmento largo puede ser menor, incrementando la prima para esos activos.

#### Aplicaciones Prácticas

Este enfoque permite explicar por qué, en ciertos periodos, la estructura de tasas presenta anomalías que no se ajustan a la simple expectativa de tasas futuras. Además, se utiliza para analizar la sensibilidad de diferentes segmentos de la curva ante cambios en la política financiera.

---

### 2.5. Teoría de la Segmentación del Mercado

#### Dinámicas Independientes entre Segmentos

La **teoría de la segmentación del mercado** propone que cada tramo del espectro temporal se comporta de manera independiente, dado que los participantes en cada segmento son en gran medida distintos y no existe movilidad perfecta entre ellos. Bajo este enfoque:

- **Cada segmento es un mercado aislado:** La oferta y la demanda en, por ejemplo, el segmento corto, no están directamente vinculadas a las condiciones del segmento largo.
- **Ausencia de condiciones de arbitraje:** Debido a restricciones institucionales o de inversión, las condiciones de no arbitraje pueden no cumplirse en forma global, lo que permite que se establezcan curvas de rendimiento disociadas.

#### Implicaciones y Críticas

Aunque este modelo puede explicar ciertos comportamientos atípicos observados en la práctica (por ejemplo, movimientos divergentes entre segmentos cortos y largos), presenta la limitación de que no permite una explicación unificada del comportamiento de la curva en su totalidad. Esto dificulta el uso de forward rates como indicadores confiables de expectativas futuras en mercados altamente segmentados.

---

### 2.6. Comparación y Relevancia Empírica

En la práctica, la estructura temporal de las tasas resulta ser el producto de una combinación de estos factores:
- **Expectativas futuras:** Aunque los forward rates incorporan información sobre la evolución de las tasas, la presencia de primas de riesgo (liquidez o hábitat) distorsiona la interpretación directa.
- **Estudios empíricos:** Los modelos dinámicos (por ejemplo, los modelos de estructura temporal afín) permiten separar en cierto grado las expectativas de las primas de riesgo. Sin embargo, la evidencia sugiere que la capacidad predictiva de los forward rates es limitada, y su efectividad depende del horizonte temporal y de las condiciones del mercado.

---

### 2.7. Implicaciones para la Política Monetaria y Estrategias de Inversión

Una comprensión profunda de estas teorías permite:
- **Diseñar estrategias de inversión más robustas:** Al identificar cuándo una tasa forward incorpora una alta prima de riesgo, se pueden ajustar las estrategias de cobertura y posicionamiento en renta fija.
- **Interpretar señales de recesión o expansión:** Por ejemplo, una curva invertida puede ser interpretada de forma diferente dependiendo de si se considera que la inversión es producto de expectativas reales o de ajustes en la prima de liquidez.
- **Orientar la política monetaria:** Los bancos centrales pueden utilizar esta información para evaluar la efectividad de sus medidas, ya que la evolución de las expectativas y las primas de riesgo reflejan la percepción del mercado sobre las condiciones económicas futuras.



## 3. Ejercicios en Python: Implementación y Análisis

### Cálculo de Tasas Forward

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calcular_tasa_forward(r1, t1, r2, t2):
    """
    Calcula la tasa forward entre dos períodos.
    
    Args:
        r1 (float): Tasa spot hasta t1 (anualizada)
        t1 (float): Tiempo hasta primer período (en años)
        r2 (float): Tasa spot hasta t2 (anualizada)
        t2 (float): Tiempo hasta segundo período (en años)
        
    Returns:
        float: Tasa forward entre t1 y t2 (anualizada)
    """
    # Fórmula de la tasa forward
    f = ((1 + r2)**t2 / (1 + r1)**t1)**(1/(t2-t1)) - 1
    return f

# Ejemplo con datos reales
curva_spot = {
    '1Y': 0.0325,  # 1 año: 3.25%
    '2Y': 0.0340,  # 2 años: 3.40%
    '3Y': 0.0360,  # 3 años: 3.60%
    '5Y': 0.0380,  # 5 años: 3.80%
    '10Y': 0.0410  # 10 años: 4.10%
}

# Convertimos a años para facilitar cálculos
plazos = {'1Y': 1, '2Y': 2, '3Y': 3, '5Y': 5, '10Y': 10}

# Calculamos tasas forward para varios períodos
forwards = {}
forwards['1Y-2Y'] = calcular_tasa_forward(curva_spot['1Y'], plazos['1Y'], 
                                         curva_spot['2Y'], plazos['2Y'])
forwards['2Y-3Y'] = calcular_tasa_forward(curva_spot['2Y'], plazos['2Y'], 
                                         curva_spot['3Y'], plazos['3Y'])
forwards['3Y-5Y'] = calcular_tasa_forward(curva_spot['3Y'], plazos['3Y'], 
                                         curva_spot['5Y'], plazos['5Y'])
forwards['5Y-10Y'] = calcular_tasa_forward(curva_spot['5Y'], plazos['5Y'], 
                                          curva_spot['10Y'], plazos['10Y'])

# Resultados
print("Tasas Forward:")
for periodo, tasa in forwards.items():
    print(f"{periodo}: {tasa:.4f} ({tasa*100:.2f}%)")
```

### Visualización de Curvas Spot y Forward

```python
# Preparamos datos para visualización
periodos_spot = list(plazos.values())
tasas_spot = list(curva_spot.values())

# Creamos períodos forward para graficar
periodos_forward = [1.5, 2.5, 4, 7.5]  # Punto medio entre períodos
tasas_forward = list(forwards.values())

# Visualización
plt.figure(figsize=(12, 6))

# Curva spot
plt.plot(periodos_spot, [tasa*100 for tasa in tasas_spot], 'o-', 
         label='Tasas Spot', color='blue', linewidth=2)

# Tasas forward
plt.plot(periodos_forward, [tasa*100 for tasa in tasas_forward], 'x--', 
         label='Tasas Forward', color='red', markersize=10, linewidth=2)

# Añadimos etiquetas
for i, periodo in enumerate(periodos_spot):
    plt.annotate(f"{tasas_spot[i]*100:.2f}%", 
                 (periodo, tasas_spot[i]*100), 
                 xytext=(5, 10), textcoords='offset points')

for i, periodo in enumerate(periodos_forward):
    plt.annotate(f"{tasas_forward[i]*100:.2f}%", 
                 (periodo, tasas_forward[i]*100), 
                 xytext=(5, -15), textcoords='offset points', color='red')

plt.title('Comparación entre Tasas Spot y Tasas Forward', fontsize=14)
plt.xlabel('Tiempo (años)', fontsize=12)
plt.ylabel('Tasa (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
```

### Estrategias de Trading Basadas en Teorías de Estructura Temporal

```python
def analizar_estrategia_curva(spot_actual, forward_implicito, spot_esperado, teoria='expectativas'):
    """
    Análisis de estrategia basada en diferentes teorías de la estructura temporal.
    
    Args:
        spot_actual (float): Tasa spot actual
        forward_implicito (float): Tasa forward implícita en la curva
        spot_esperado (float): Tasa spot esperada según el trader
        teoria (str): Teoría a aplicar ('expectativas', 'liquidez', 'habitat', 'segmentacion')
        
    Returns:
        str: Recomendación de estrategia
    """
    diferencia = forward_implicito - spot_esperado
    
    if teoria == 'expectativas':
        # Teoría de expectativas puras - forward = expectativa futura
        if diferencia > 0.0010:  # Más de 10 puntos básicos
            return "VENDER: Forward sobrevalorado según expectativas puras"
        elif diferencia < -0.0010:
            return "COMPRAR: Forward infravalorado según expectativas puras"
        else:
            return "MANTENER: Forward alineado con expectativas puras"
            
    

# Ejemplo práctico
forward_1y2y = forwards['1Y-2Y']
expectativa_trader = 0.0330  # El trader espera 3.30% para el período 1Y-2Y

print("\nAnálisis de estrategias según distintas teorías:")
print(f"Tasa forward implícita 1Y-2Y: {forward_1y2y:.4f} ({forward_1y2y*100:.2f}%)")
print(f"Expectativa del trader: {expectativa_trader:.4f} ({expectativa_trader*100:.2f}%)")

for teoria in ['expectativas']:
    estrategia = analizar_estrategia_curva(curva_spot['1Y'], forward_1y2y, expectativa_trader, teoria)
    print(f"Según teoría de {teoria}: {estrategia}")
```
