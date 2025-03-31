# Clase 05: Renta Fija Avanzada - Pricing vs. Valuation y Medidas de Sensibilidad

**Módulo:** 1 - Renta Fija
**Fecha:** (02-abr-25 - *Nota: Usaremos esta como fecha de análisis*)
**Objetivos de Aprendizaje:**

1.  **Diferenciar conceptual y prácticamente entre *pricing* y *valoración* de instrumentos de renta fija.**
2.  **Comprender la implicancia de IFRS 9 en la contabilización y reporte (Amortized Cost, FVOCI, FVPL).**
3.  **Calcular e interpretar las medidas clave de sensibilidad al riesgo de tasa de interés: Duration (Macaulay, Modificada) y Convexidad.**
4.  **Estimar el impacto de cambios en las tasas de interés sobre el precio de un bono utilizando Duration y Convexidad.**
5.  **Graficar y analizar la relación precio-yield.**
6.  **Evaluar escenarios de Mark-to-Market (MtM) y Retorno Total para un inversionista.**
7.  **Introducir el concepto de Curva Cero Cupón (Spot) y el método de Bootstrapping.**
8.  **Presentar brevemente los modelos paramétricos de curva de tasas: Nelson-Siegel y Svensson.**


---

## Sección 1: Pricing vs. Valuation en Renta Fija

### 1.1. La Distinción Fundamental

*   **Valoración (Valuation):**
    *   **Concepto:** Estimación del *valor intrínseco* o "justo" de un activo, basado en sus fundamentos: flujos de caja esperados, riesgo inherente y el rendimiento requerido por el mercado para activos similares.
    *   **Enfoque:** ¿Cuánto *debería* valer el bono? Se basa en modelos (DCF es el principal en renta fija), supuestos sobre el futuro y análisis de crédito/riesgo.
    *   **Perspectiva:** Más a largo plazo, busca identificar si un activo está sobre o infravalorado respecto a su "verdadero" valor económico.
    *   **Ejemplo:** Calcular el valor presente de los flujos de caja de BTP0450326 usando una tasa de descuento que refleje nuestro análisis *propio* del riesgo crediticio del gobierno y las condiciones macroeconómicas esperadas.

*   **Pricing:**
    *   **Concepto:** Determinación del *precio de mercado* actual de un activo, basado en la intersección de la oferta y la demanda en un momento dado.
    *   **Enfoque:** ¿A cuánto *se está transando* el bono *ahora*? Refleja la percepción *agregada* del mercado sobre el valor y el riesgo, liquidez, sentimiento y factores técnicos.
    *   **Perspectiva:** Corto plazo, observable, utilizado para la ejecución de transacciones y el Mark-to-Market.
    *   **Ejemplo:** El precio de 99.4969 para BTP0450326 con una TIR (Yield-to-Maturity) de 5.0552% en la fecha 16/01/2025 es un *precio* de mercado observado. Es el resultado del consenso del mercado en ese instante. Si mi intención fuera adquirir ese bono podría transarlo en el mercado spot a ese valor sin mayores problemas asumiendo un bono líquido.

*   **¿Por qué la diferencia es crucial?**
    *   **Gestión de Portafolios:** Un gestor puede comprar un bono cuyo *precio* es inferior a su *valoración* interna (oportunidad de valor).
    *   **Gestión de Riesgos:** El *precio* fluctúa con las tasas de mercado (riesgo de interés), afectando el valor de mercado del portafolio. La *valoración* puede ser más estable si los fundamentos no cambian drásticamente.
    *   **Contabilidad y Regulación:** Aquí entra IFRS 9.

### 1.2. Implicaciones de IFRS 9 (Normativa y Fuentes)

*   **IFRS 9 o NIIF9 (Fuente: IASB):** Establece cómo clasificar y medir los activos financieros. La clasificación depende del **modelo de negocio** de la entidad para gestionar los activos y las **características de los flujos de efectivo contractuales** del activo (SPPI - Solely Payments of Principal and Interest).

    *   **Amortized Cost (AC):**
        *   **Modelo de Negocio:** Hold-to-Collect (Mantener para cobrar flujos contractuales).
        *   **Medición:** Costo inicial menos repagos de principal, más/menos amortización acumulada de cualquier diferencia entre el costo inicial y el valor al vencimiento (usando el método de interés efectivo - EIR), menos provisiones por pérdidas crediticias.
        *   **Relación con Pricing/Valuation:** Más cercano a una *valoración* inicial que se amortiza. Los cambios diarios del *precio* de mercado no impactan directamente el P&L, solo el riesgo de crédito.

    *   **Fair Value through Other Comprehensive Income (FVOCI):**
        *   **Modelo de Negocio:** Hold-to-Collect *and* Sell (Cobrar flujos y también vender).
        *   **Medición:** Se mide a *Fair Value* (Precio de Mercado) en el balance. Los cambios en Fair Value se reconocen en *Other Comprehensive Income* (OCI), excepto el ingreso por intereses (calculado con EIR), dividendos y pérdidas por deterioro, que van a P&L. Al vender, la ganancia/pérdida acumulada en OCI se reclasifica a P&L.
        *   **Relación con Pricing/Valuation:** Híbrido. El valor reportado es el *precio* de mercado, pero el reconocimiento de ingresos sigue una lógica de *valoración* (EIR).

    *   **Fair Value through Profit or Loss (FVPL):**
        *   **Modelo de Negocio:** Residual (Trading, mantenidos para negociación, o no cumplen criterios AC/FVOCI).
        *   **Medición:** Se mide a *Fair Value* (Precio de Mercado). Todos los cambios, incluyendo intereses y fluctuaciones de precio, van directamente a P&L.
        *   **Relación con Pricing/Valuation:** Directamente ligado al *pricing* de mercado. Es el Mark-to-Market puro.

*   **Relevancia Práctica (Fuentes: CFA Institute Curriculum, GARP FRM Handbook):** La correcta clasificación bajo IFRS 9 afecta la volatilidad del P&L y del patrimonio de una entidad financiera, las métricas de capital regulatorio y la forma en que se gestiona y presenta el riesgo de tasa de interés. La distinción pricing/valuation es central para entender estas implicaciones.

**Discusión Interactiva:**
*   ¿Cómo clasificarían probablemente un banco comercial o una aseguradora al bono BTP0450326 si su intención es mantenerlo hasta el vencimiento para calzar pasivos? (Probablemente AC o FVOCI).
*   ¿Y si fuera un hedge fund especulando con movimientos de tasas a corto plazo? (Probablemente FVPL).
*   ¿Qué impacto tiene la elección en la volatilidad de resultados reportados?

---

## Sección 2: Medidas de Riesgo y Sensibilidad

El *precio* de un bono es sensible a cambios en las tasas de interés de mercado (yield). Necesitamos cuantificar esta sensibilidad.

### 2.1. La Relación Inversa Precio-Yield

Recordatorio básico: El precio de un bono es el valor presente de sus flujos de caja futuros, descontados a la tasa de rendimiento requerida por el mercado (YTM o TIR).
$$ P = \sum_{t=1}^{N} \frac{CF_t}{(1 + y/k)^{t_k}} + \frac{Par}{(1 + y/k)^{N_k}} $$
Donde:
*   `P` = Precio
*   `CF_t` = Flujo de caja (cupón) en el período t
*   `Par` = Valor Par/Nominal al vencimiento
*   `y` = YTM (TIR) anual
*   `k` = Frecuencia de pago de cupones por año
*   `N` = Número total de períodos de cupón
*   `t_k`, `N_k` = Tiempo ajustado por frecuencia

Si `y` aumenta, el denominador crece, y el `P` disminuye (y viceversa). Esta relación no es lineal.

### 2.2. Duration

*   **Macaulay Duration (Fuente: Fabozzi):**
    *   **Concepto:** Vida media ponderada de los flujos de caja del bono, donde la ponderación es el valor presente de cada flujo como proporción del precio total. Mide el "tiempo promedio" hasta recibir el valor del bono.
    *   **Fórmula (para YTM discreto):**
        $$ D_{mac} = \frac{\sum_{t=1}^{N} t \times \frac{CF_t}{(1 + y/k)^{t_k}}}{\sum_{t=1}^{N} \frac{CF_t}{(1 + y/k)^{t_k}}} = \frac{\sum_{t=1}^{N} t \times PV(CF_t)}{P} $$
        *Unidades: Años*

*   **Modified Duration:**
    *   **Concepto:** Medida de la sensibilidad porcentual del precio del bono ante un cambio unitario (pequeño) en el yield. Es la primera derivada del precio respecto al yield, escalada por el precio.
    *   **Fórmula:**
        $$ D_{mod} = -\frac{1}{P} \frac{\partial P}{\partial y} \approx \frac{D_{mac}}{(1 + y/k)} $$
    *   **Interpretación:** Un bono con $D_{mod} = 5$ años significa que por cada aumento de 1% (100 bps) en el yield, su precio *aproximadamente* caerá un 5%.
        $$ \frac{\Delta P}{P} \approx -D_{mod} \times \Delta y $$

### 2.3. Convexity

*   **Concepto:** Mide la curvatura de la relación precio-yield. La aproximación lineal de la Duration Modificada comete errores, especialmente para cambios grandes en el yield. La convexidad captura este error (segunda derivada).
    *   Una mayor convexidad es *beneficiosa* para el tenedor del bono: el precio sube más cuando los yields caen de lo que baja cuando los yields suben en la misma magnitud.
*   **Fórmula:**
    $$ C = \frac{1}{P} \frac{\partial^2 P}{\partial y^2} \approx \frac{\sum_{t=1}^{N} \frac{CF_t}{(1 + y/k)^{t_k+2}} \times t_k \times (t_k+1) / k^2}{P} $$
    *Unidades: Años² (a menudo se reporta escalada)*

*   **Ajuste del Precio por Duration y Convexidad:**
    $$ \frac{\Delta P}{P} \approx -D_{mod} \times \Delta y + \frac{1}{2} \times C \times (\Delta y)^2 $$

### 2.4. Aplicación con Python calculo de bono

**Supuestos:**
*   Fecha Valoración: 16-Ene-2025
*   Fecha Vencimiento: 01-Mar-2026 (Estimado de 1.12 años residual)
*   Cupón: 4.5% anual, pagadero semestral (1 Mar y 1 Sep)
*   Par: 100
*   YTM (TIR): 5.0552% (0.050552)
*   Precio Mercado: 99.4969 (Verificaremos con cálculo)
*   Fechas de Flujos Pendientes: 01-Mar-2025, 01-Sep-2025, 01-Mar-2026 (Vencimiento)

```python
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# --- Datos del Bono BTP0450326 (con supuestos) ---
val_date = date(2025, 1, 16)
maturity_date = date(2026, 3, 1)
coupon_rate = 0.045
par_value = 100
ytm = 0.050552
frequency = 2 # Pagos semestrales

# --- Calcular Flujos de Caja y Fechas ---
# Próximas fechas de cupón teóricas: 1 Sep 2024, 1 Mar 2025, 1 Sep 2025, 1 Mar 2026
# Flujos restantes desde val_date:
cash_flow_dates = [date(2025, 3, 1), date(2025, 9, 1), date(2026, 3, 1)]
cash_flows = np.array([coupon_rate * par_value / frequency] * (len(cash_flow_dates) - 1) + \
                      [par_value + coupon_rate * par_value / frequency])

# --- Calcular tiempos hasta cada flujo (en años) ---
# Usando convención ACT/365 para precisión
time_to_cfs = np.array([(cf_date - val_date).days / 365.0 for cf_date in cash_flow_dates])

# --- Calcular Precio (Verificación) ---
discount_factors = (1 + ytm / frequency)**(-time_to_cfs * frequency)
calculated_price = np.sum(cash_flows * discount_factors)

print(f"Fecha Valoración: {val_date}")
print(f"Fecha Vencimiento: {maturity_date}")
print(f"Tasa Cupón: {coupon_rate*100:.2f}%")
print(f"YTM (TIR): {ytm*100:.4f}%")
print(f"Fechas Flujos Restantes: {cash_flow_dates}")
print(f"Montos Flujos Restantes: {cash_flows}")
print(f"Tiempos hasta Flujos (años): {time_to_cfs}")
print(f"Precio Calculado: {calculated_price:.4f}") # Debería ser cercano a 99.4969

# --- Calcular Macaulay Duration ---
pv_cfs = cash_flows * discount_factors
weighted_time = time_to_cfs * pv_cfs
macaulay_duration = np.sum(weighted_time) / calculated_price
print(f"Macaulay Duration: {macaulay_duration:.4f} años")

# --- Calcular Modified Duration ---
modified_duration = macaulay_duration / (1 + ytm / frequency)
print(f"Modified Duration: {modified_duration:.4f}")

# --- Calcular Convexity ---
# Usando fórmula aproximada (chequear textos para fórmula exacta para semianual)
# Ojo: La fórmula de convexidad puede variar ligeramente entre textos. Usamos una común.
convexity_term = cash_flows * discount_factors * time_to_cfs * (time_to_cfs + 1/frequency) # Ajuste simple por frecuencia
convexity = np.sum(convexity_term) / (calculated_price * (1 + ytm / frequency)**2)
print(f"Convexity: {convexity:.4f}") # Unidad: años^2 (a veces se escala)

# --- Graficar Relación Precio-Yield ---
yields = np.linspace(ytm - 0.02, ytm + 0.02, 50) # Rango de +/- 200 bps
prices = []
for y in yields:
    discount_factors_y = (1 + y / frequency)**(-time_to_cfs * frequency)
    prices.append(np.sum(cash_flows * discount_factors_y))

plt.figure(figsize=(10, 6))
plt.plot(yields * 100, prices, label='Precio Real del Bono')
plt.xlabel('Yield (TIR) (%)')
plt.ylabel('Precio del Bono ($)')
plt.title(f'Relación Precio-Yield para BTP0450326 (Val Date: {val_date})')
plt.grid(True)

# Añadir punto actual
plt.plot(ytm * 100, calculated_price, 'ro', label=f'Precio Actual ({calculated_price:.2f}) @ {ytm*100:.2f}%')

# Añadir línea tangente (aproximación por Duration)
price_change_approx_dur = -modified_duration * (yields - ytm) * calculated_price
tangent_prices = calculated_price + price_change_approx_dur
plt.plot(yields * 100, tangent_prices, 'g--', label='Aprox. por Duration')

plt.legend()
plt.show()

# --- Estimación de Cambio de Precio ---
delta_y = 0.01 # Cambio de +100 bps (1%)

# Usando solo Duration Modificada
price_change_pct_dur = -modified_duration * delta_y
price_change_abs_dur = price_change_pct_dur * calculated_price
new_price_est_dur = calculated_price + price_change_abs_dur

# Usando Duration + Convexidad
price_change_pct_conv = -modified_duration * delta_y + 0.5 * convexity * (delta_y**2)
price_change_abs_conv = price_change_pct_conv * calculated_price
new_price_est_conv = calculated_price + price_change_abs_conv

# Precio Real con nuevo Yield
new_ytm = ytm + delta_y
discount_factors_new = (1 + new_ytm / frequency)**(-time_to_cfs * frequency)
actual_new_price = np.sum(cash_flows * discount_factors_new)

print(f"\n--- Estimación de Impacto por subida de 100 bps ({delta_y*100:.0f} bps) ---")
print(f"Nuevo YTM: {new_ytm*100:.4f}%")
print(f"Precio Estimado (Solo Duration): {new_price_est_dur:.4f}")
print(f"Precio Estimado (Duration + Convexidad): {new_price_est_conv:.4f}")
print(f"Precio Real Calculado: {actual_new_price:.4f}")
print(f"Error (Solo Duration): {abs(new_price_est_dur - actual_new_price):.4f}")
print(f"Error (Duration + Convexidad): {abs(new_price_est_conv - actual_new_price):.4f}")

```

**Discusión Interactiva (5 min):**
*   Analizar el gráfico: ¿Se observa la convexidad? ¿Cómo se compara la aproximación lineal con la curva real?
*   Comparar los errores en la estimación de precio. ¿Cuándo se vuelve más importante el ajuste por convexidad? (Cambios grandes de yield, bonos de largo plazo).
*   ¿Qué implica la Duration calculada (aprox. 1.09 años en la captura, nuestro cálculo ~1.07) para un gestor de portafolio? (Baja sensibilidad relativa al riesgo de tasa de interés).

---

## Sección 3: Mark-to-Market y Escenarios de Retorno

Vamos a simular qué ocurre con la inversión en BTP0450326 bajo dos escenarios, considerando la fecha de la clase (07-Abr-2025) como un punto de evaluación intermedio.

**Escenario Base:**
*   Compra: 16-Ene-2025
*   Precio Compra: 99.4969 (por 100 de nominal)
*   YTM Compra: 5.0552%
*   Fecha Evaluación Intermedia: 07-Abr-2025
*   Fecha Vencimiento: 01-Mar-2026

**Supuesto Clave:** Asumamos que el 07-Abr-2025, debido a cambios en las expectativas de inflación o política monetaria, la YTM de mercado para este bono **sube a 5.75%**.

### 3.1. Pricing y Valoración en Diferentes Momentos

*   **Al Inicio (16-Ene-2025):**
    *   Precio (Pricing): 99.4969
    *   Valoración (Contable si es AC): Costo inicial 99.4969 (más costos de transacción si aplica).
*   **En Fecha Intermedia (07-Abr-2025):**
    *   Necesitamos recalcular el precio (Pricing) con el nuevo YTM (5.75%) y el tiempo restante hasta el vencimiento.
    *   Valoración (Contable si es AC): Sería el costo amortizado. Calculado usando la TIR inicial (5.0552%). No coincide con el precio de mercado.
    *   Valoración (Contable si es FVOCI/FVPL): Sería el nuevo precio de mercado (Fair Value).

*   **Al Vencimiento (01-Mar-2026):**
    *   Precio (Pricing): Converge a Par (100).
    *   Valoración (Contable AC/FVOCI): Converge a Par (100) a través de la amortización/devengo de intereses.

### 3.2. Cálculo de Retornos

*   **Escenario A: Venta el 07-Abr-2025 (Mark-to-Market)**
    *   Necesitamos el precio de venta y el interés devengado (accrued interest).
    *   Retorno = (Precio Venta + Interés Devengado - Precio Compra) / Precio Compra

*   **Escenario B: Mantener hasta el Vencimiento (Hold-to-Maturity)**
    *   Retorno = (Suma de Cupones Recibidos + (Valor Par - Precio Compra)) / Precio Compra
    *   Este retorno *debería* aproximarse al YTM inicial (5.0552%), asumiendo que los cupones se reinvierten a esa misma tasa (supuesto clave del YTM).

### 3.3. Aplicación con Python

```python
# --- Continuación del script anterior ---

# --- Escenario A: Venta el 07-Abr-2025 ---
eval_date = date(2025, 4, 7)
new_ytm_eval = 0.0575 # YTM sube a 5.75%

# Recalcular tiempo a flujos desde eval_date
time_to_cfs_eval = np.array([(cf_date - eval_date).days / 365.0 for cf_date in cash_flow_dates])
# Filtrar flujos pasados (ninguno en este caso, pero buena práctica)
valid_indices = time_to_cfs_eval >= 0
time_to_cfs_eval = time_to_cfs_eval[valid_indices]
cash_flows_eval = cash_flows[valid_indices]

# Calcular precio de venta en eval_date con nuevo YTM
discount_factors_eval = (1 + new_ytm_eval / frequency)**(-time_to_cfs_eval * frequency)
selling_price = np.sum(cash_flows_eval * discount_factors_eval)

# Calcular Interés Devengado (Accrued Interest)
# Último cupón: 1 Sep 2024. Próximo cupón: 1 Mar 2025.
# La fecha de evaluación (7 Abr) es DESPUÉS del cupón del 1 Mar 2025.
# Por tanto, el devengo es desde el 1 Mar 2025 hasta el 7 Abr 2025.
last_coupon_date = date(2025, 3, 1)
days_since_last_coupon = (eval_date - last_coupon_date).days
# Asumamos un período de cupón estándar de ~182.5 días (365/2)
# O calcular días exactos entre 1 Mar 25 y 1 Sep 25
days_in_period = (date(2025, 9, 1) - date(2025, 3, 1)).days
coupon_amount = coupon_rate * par_value / frequency
accrued_interest = (days_since_last_coupon / days_in_period) * coupon_amount

purchase_price = calculated_price # Usamos el precio calculado para consistencia

# Retorno Total Escenario A (sin anualizar)
total_proceeds_A = selling_price + accrued_interest + coupon_amount # Sumamos el cupón cobrado el 1 Mar 2025
return_A = (total_proceeds_A - purchase_price) / purchase_price

# Tiempo transcurrido en años
holding_period_A = (eval_date - val_date).days / 365.0
# Retorno Anualizado (Simple)
annualized_return_A = (1 + return_A)**(1/holding_period_A) - 1

print(f"\n--- Escenario A: Venta el {eval_date} ---")
print(f"Nuevo YTM de Mercado: {new_ytm_eval*100:.4f}%")
print(f"Precio de Venta (Clean Price): {selling_price:.4f}")
print(f"Interés Devengado: {accrued_interest:.4f}")
print(f"Cupón Cobrado el 01-Mar-2025: {coupon_amount:.4f}")
print(f"Retorno Total del Período ({holding_period_A:.3f} años): {return_A*100:.2f}%")
print(f"Retorno Anualizado (aprox): {annualized_return_A*100:.2f}%")

# --- Escenario B: Mantener hasta Vencimiento (01-Mar-2026) ---
total_coupons_received = np.sum(cash_flows[:-1]) # Suma de todos los cupones
final_payment = cash_flows[-1] # Último cupón + Par

# Retorno Total Escenario B (sin anualizar y sin reinversión)
# Nota: Esto es el Holding Period Return, no el YTM realizado (que depende de reinversión)
return_B_hpr = (total_coupons_received + (par_value - purchase_price)) / purchase_price

# Tiempo total de tenencia
holding_period_B = (maturity_date - val_date).days / 365.0
# Retorno Anualizado (usando HPR, aproxima YTM si reinversión fuera a YTM)
annualized_return_B = ( (total_coupons_received + par_value) / purchase_price )**(1/holding_period_B) - 1


print(f"\n--- Escenario B: Mantener hasta {maturity_date} ---")
print(f"Cupones Totales Recibidos: {total_coupons_received + coupon_amount:.4f} (incluye el del final)") # Sumamos el cupón del último flujo
print(f"Ganancia/Pérdida de Capital: {par_value - purchase_price:.4f}")
print(f"Retorno Total del Período ({holding_period_B:.3f} años): {return_B_hpr*100:.2f}% (sin reinversión)")
print(f"Retorno Anualizado (YTM realizado aprox.): {annualized_return_B*100:.2f}%") # Cercano al YTM inicial
print(f"(YTM Inicial era: {ytm*100:.4f}%)")

```

**Discusión Interactiva (5 min):**
*   ¿Por qué el retorno en el Escenario A es negativo o bajo? (Impacto de la subida de tasas en el precio de venta).
*   ¿Por qué el retorno anualizado en el Escenario B se acerca al YTM inicial? (Se realizaron todos los flujos contractuales; la diferencia se debe a la reinversión y posible error de redondeo/convención de días).
*   Relacionar esto con IFRS 9: ¿Cómo afectaría el P&L y OCI en cada escenario si el bono estuviera clasificado como FVPL vs. FVOCI vs. AC?

---

## Sección 4: Construcción de la Curva Cero Cupón (Spot)

### 4.1. Concepto

*   La YTM de un bono con cupón es un promedio ponderado de las tasas spot relevantes para cada uno de sus flujos.
*   La **Curva Cero Cupón (Spot)** representa la tasa de interés (yield) para un pago único (cero cupón) a recibir en una fecha futura específica. Es la tasa de descuento "pura" para cada vencimiento.
*   Es teóricamente superior para valorar bonos, ya que cada flujo se descuenta a la tasa apropiada para su vencimiento.
*   No se observa directamente para todos los plazos, por lo que se *deriva* de los precios de bonos con cupón (generalmente bonos soberanos líquidos).

### 4.2. Método de Bootstrapping

Proceso iterativo para extraer tasas spot (z) a partir de los precios de bonos con cupón (YTMs o precios de mercado).

**Idea:**
1.  Usar el bono más corto (ej. Letra del Tesoro a 6 meses) cuyo precio da directamente la tasa spot a 6 meses ($P = Par / (1 + z_1/2)^1$).
2.  Usar el siguiente bono (ej. Bono a 1 año con cupón semestral). Su precio es:
    $P = \frac{C/2}{(1 + z_1/2)^1} + \frac{Par + C/2}{(1 + z_2/2)^2}$
    Conocemos $P$, $C$, $Par$, y $z_1$ (del paso anterior). Despejamos $z_2$ (la tasa spot a 1 año).
3.  Continuar con bonos de plazos sucesivamente más largos, usando las tasas spot ya calculadas para descontar los flujos tempranos y despejando la nueva tasa spot del último flujo.

### 4.3. Ejemplo Simplificado con Python

Supongamos que tenemos los siguientes bonos del gobierno (hipotéticos) y sus YTMs:

*   Bono 0.5 años: Cupón 0%, YTM = 4.0%
*   Bono 1.0 años: Cupón 5%, Pago Semestral, YTM = 4.5%
*   Bono 1.5 años: Cupón 6%, Pago Semestral, YTM = 4.8%

```python
from scipy.optimize import newton

# --- Datos Hipotéticos Bonos Gobierno ---
# Plazo (años), Tasa Cupón, Frecuencia, YTM
bond_data = {
    0.5: {'coupon': 0.00, 'freq': 1, 'ytm': 0.040},
    1.0: {'coupon': 0.05, 'freq': 2, 'ytm': 0.045},
    1.5: {'coupon': 0.06, 'freq': 2, 'ytm': 0.048},
}
par = 100
spot_rates = {} # Diccionario para guardar las tasas spot calculadas

# --- Calcular Precios desde YTMs (si no los tuviéramos) ---
prices = {}
for t, data in bond_data.items():
    freq = data['freq']
    coupon = data['coupon'] * par / freq
    ytm_bond = data['ytm']
    n_periods = int(t * freq)
    cf = np.array([coupon] * (n_periods - 1) + [par + coupon])
    times = np.arange(1, n_periods + 1) / freq
    discount_factors = (1 + ytm_bond / freq)**(-times * freq) # Ojo: Esto es descuento YTM, no spot
    prices[t] = np.sum(cf * discount_factors)
    print(f"Precio Bono {t} años (calculado desde YTM): {prices[t]:.4f}")


# --- Bootstrapping ---

# 1. Bono 0.5 años (T-Bill)
t = 0.5
price_05 = prices[t] # Usamos el precio calculado (o usaríamos precio mercado)
# P = Par / (1 + z_0.5/1)^0.5  -> para freq=1
# O si se considera anualizado: P = Par / (1 + z_0.5)**0.5
# O si YTM es BEY (Bond Equivalent Yield), z_0.5 = YTM (asumamos esto por simplicidad)
z_05 = bond_data[t]['ytm']
spot_rates[t] = z_05
print(f"\nSpot Rate {t*100:.0f} meses: {z_05*100:.4f}%")

# 2. Bono 1.0 año
t = 1.0
price_10 = prices[t]
coupon_10 = bond_data[t]['coupon'] * par / bond_data[t]['freq']
freq_10 = bond_data[t]['freq']
# P = C1/(1+z_0.5/2)^1 + (Par+C2)/(1+z_1.0/2)^2
# Necesitamos la tasa spot semestral z_0.5 / 2. Derivada de z_0.5 anual.
# (1 + z_0.5) = (1 + z_0.5_semi)**2 => z_0.5_semi = sqrt(1+z_0.5)-1
z_05_semi = (1 + spot_rates[0.5])**(1/freq_10) - 1

# Ecuación: price_10 = coupon_10/(1+z_0.5_semi)^1 + (par+coupon_10)/(1+z_1.0_semi)^2
# Despejar z_1.0_semi
term1_pv = coupon_10 / (1 + z_05_semi)**1
z_10_semi = ( (par + coupon_10) / (price_10 - term1_pv) )**(1/2) - 1
# Convertir a tasa anual (BEY-like o EAR)
# BEY = z_1.0_semi * 2
# EAR = (1 + z_1.0_semi)**2 - 1
z_10_annual = (1 + z_10_semi)**freq_10 - 1 # Usamos EAR
spot_rates[t] = z_10_annual
print(f"Spot Rate {t*100:.0f} meses: {z_10_annual*100:.4f}% (EAR)")


# 3. Bono 1.5 años
t = 1.5
price_15 = prices[t]
coupon_15 = bond_data[t]['coupon'] * par / bond_data[t]['freq']
freq_15 = bond_data[t]['freq']
# P = C1/(1+z_0.5_semi)^1 + C2/(1+z_1.0_semi)^2 + (Par+C3)/(1+z_1.5_semi)^3
# Usamos las tasas semestrales z_0.5_semi y z_1.0_semi ya calculadas
term1_pv_15 = coupon_15 / (1 + z_05_semi)**1
term2_pv_15 = coupon_15 / (1 + z_10_semi)**2 # Usando la z_1.0_semi calculada antes

# Despejar z_1.5_semi
z_15_semi = ( (par + coupon_15) / (price_15 - term1_pv_15 - term2_pv_15) )**(1/3) - 1
# Convertir a tasa anual (EAR)
z_15_annual = (1 + z_15_semi)**freq_15 - 1 # Usamos EAR
spot_rates[t] = z_15_annual
print(f"Spot Rate {t*100:.0f} meses: {z_15_annual*100:.4f}% (EAR)")

print("\nCurva Spot Calculada (EAR):")
for t, rate in spot_rates.items():
    print(f"  {t:.1f} años: {rate*100:.4f}%")

```
*(Nota: El cálculo exacto de bootstrapping puede requerir solvers numéricos para casos más complejos o si las tasas base no son directamente YTMs cero cupón. La conversión entre tasas semestrales y anuales (BEY vs EAR) debe ser consistente).*

**Discusión Interactiva (2 min):**
*   ¿Qué forma tiene la curva spot resultante en este ejemplo? (Ascendente).
*   ¿Por qué es importante la curva spot para valoración y gestión de riesgos? (Descuento preciso, cálculo de forwards, valoración de derivados de tasa).

---

## Sección 5: Introducción a Modelos Paramétricos de Curva

El bootstrapping puede generar curvas "ruidosas" o con gaps si los datos de bonos son imperfectos o escasos. Los modelos paramétricos buscan ajustar una función matemática suave a los datos observados.

### 5.1. Nelson-Siegel (1987)

*   **Objetivo:** Modelar la curva de tasas forward instantánea (y por integración, la curva spot) usando pocos parámetros con interpretación económica.
*   **Fórmula (Tasa Forward Instantánea f(m) a madurez m):**
    $$ f(m) = \beta_0 + \beta_1 \exp\left(-\frac{m}{\tau_1}\right) + \beta_2 \left( \frac{m}{\tau_1} \exp\left(-\frac{m}{\tau_1}\right) \right) $$
*   **Parámetros:**
    *   $\beta_0$: Factor de **Nivel** (Level) - Contribución a largo plazo, hacia dónde converge la tasa.
    *   $\beta_1$: Factor de **Pendiente** (Slope) - Contribución a corto plazo (diferencia corto vs largo plazo).
    *   $\beta_2$: Factor de **Curvatura** (Curvature) - Modela la "joroba" o forma de U invertida en plazos medios.
    *   $\tau_1$: Factor de **Escala/Decaimiento** - Controla dónde ocurre el máximo de la joroba y la velocidad de convergencia.
*   **Ventajas:** Parsimonioso (pocos parámetros), interpretación intuitiva, buen ajuste general.

### 5.2. Nelson-Siegel-Svensson (1994)

*   **Objetivo:** Mejorar el ajuste de Nelson-Siegel añadiendo más flexibilidad, especialmente para curvas con doble "joroba" o formas más complejas.
*   **Fórmula (Tasa Forward Instantánea f(m)):**
    $$ f(m) = \beta_0 + \beta_1 \exp\left(-\frac{m}{\tau_1}\right) + \beta_2 \left( \frac{m}{\tau_1} \exp\left(-\frac{m}{\tau_1}\right) \right) + \beta_3 \left( \frac{m}{\tau_2} \exp\left(-\frac{m}{\tau_2}\right) \right) $$
*   **Parámetros Adicionales:**
    *   $\beta_3$: Segundo Factor de **Curvatura**.
    *   $\tau_2$: Segundo Factor de **Escala/Decaimiento**.
*   **Ventajas:** Mayor flexibilidad y capacidad de ajuste a formas de curva más complejas.
*   **Desventajas:** Más parámetros (6 vs 4), posible sobreajuste (overfitting), interpretación menos directa que N-S.

**Propósito General:**
*   **Suavizado (Smoothing):** Obtener curvas sin el ruido del bootstrapping.
*   **Interpolación/Extrapolación:** Estimar tasas para vencimientos donde no hay datos directos.
*   **Análisis:** Descomponer movimientos de la curva en cambios de nivel, pendiente y curvatura.
*   **Input para otros modelos:** Modelos de riesgo, pricing de derivados.

**Próximos Pasos (Introducción):** En sesiones futuras podríamos explorar la estimación de estos parámetros y su uso en modelos dinámicos de tasas de interés.

---

## Conclusiones y Preguntas (Buffer / Final)

*   Hemos diferenciado **Pricing** (mercado, observable, corto plazo) de **Valuation** (intrínseco, modelado, largo plazo), vinculándolo a **IFRS 9**.
*   Calculamos e interpretamos **Duration** y **Convexidad** como medidas esenciales de riesgo de tasa de interés para el bono BTP0450326.
*   Simulamos escenarios de **Mark-to-Market** y **Hold-to-Maturity**, mostrando el impacto real en el retorno del inversionista.
*   Introdujimos la **Curva Spot Cero Cupón** y el **Bootstrapping** como método para derivarla.
*   Presentamos los modelos de **Nelson-Siegel** y **Svensson** como herramientas para modelar la curva de forma paramétrica.


**Fuentes Principales Citadas:**
1.  **IASB (International Accounting Standards Board):** Creador de la normativa IFRS 9.
2.  **Fabozzi, F. J.:** Autor prolífico y referente en Renta Fija (e.g., "Bond Markets, Analysis, and Strategies"). Creador/divulgador de teoría.
3.  **CFA Institute:** Curriculum oficial, fundamental para la aplicación práctica y estándares profesionales.
4.  **GARP (Global Association of Risk Professionals):** Curriculum FRM, enfocado en la gestión de riesgos financieros, incluyendo riesgo de tasa de interés.
