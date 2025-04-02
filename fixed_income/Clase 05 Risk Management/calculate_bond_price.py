import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots
from loguru import logger


# pip install loguru
# pip install matplotlib



# Usar SciencePlots para el estilo de los gráficos
plt.style.use(["science", "ieee"])


def price_of_bond(face_value, coupon_rate, maturity, yield_rate, frequency=1):
    """
    Calcula el precio de un bono que paga cupón de forma periódica.

    Parámetros:
      - face_value: Valor nominal del bono.
      - coupon_rate: Tasa cupón anual (por ejemplo, 0.03 para 3%).
      - maturity: Plazo del bono en años.
      - yield_rate: Tasa de rendimiento exigida (yield) anual en forma decimal.
      - frequency: Número de pagos de cupón al año (default=1).

    Retorna:
      - precio del bono.
    """
    n_periods = maturity * frequency
    coupon = face_value * coupon_rate / frequency
    t = np.arange(1, n_periods + 1)
    price = (
            np.sum(coupon / (1 + yield_rate / frequency) ** t) + 
            # Suma de la lista de valores presentes de cada cupon 
            (face_value / (1 + yield_rate / frequency) ** n_periods) 
            # VP del nominal
    )
    return price


def plot_price_yield_relationship(
    par=100,
    coupon_rate=0.03,
    maturity=3,
    frequency=1,
    yield_min=0.001,
    yield_max=0.10,
    num_points=200,
):
    """
    Grafica la relación entre el precio del bono y la tasa de rendimiento para un bono con parámetros definidos.

    Parámetros:
      - par: Valor nominal del bono.
      - coupon_rate: Tasa cupón anual.
      - maturity: Plazo en años.
      - frequency: Frecuencia de pagos al año.
      - yield_min, yield_max: Rango mínimo y máximo de tasas de rendimiento a evaluar.
      - num_points: Número de puntos para evaluar en el rango.
    """
    yield_rates = np.linspace(yield_min, yield_max, num_points)
    prices = [
        price_of_bond(par, coupon_rate, maturity, y, frequency) for y in yield_rates
    ]

    # Calcular el precio "a la par" (cuando yield == coupon_rate)
    par_price = price_of_bond(par, coupon_rate, maturity, coupon_rate, frequency)
    # Encontrar el índice más cercano al yield cupón
    idx_par = np.argmin(np.abs(yield_rates - coupon_rate))

    plt.figure(figsize=(8, 5))
    plt.plot(
        yield_rates * 100,
        prices,
        label=f"Bono {coupon_rate*100:.0f}% - {maturity} años",
    )
    plt.scatter(
        [yield_rates[idx_par] * 100],
        [par_price],
        color="red",
        zorder=5,
        label=f"Precio a la par ({coupon_rate*100:.1f}%)",
    )
    plt.xlabel("Tasa de rendimiento (%)")
    plt.ylabel("Precio del bono")
    plt.title("Relación entre Precio e Interés para un Bono")
    plt.grid(True)
    plt.legend()
    plt.show()


def compare_bond_cash_flows(
    par=100, coupon_rate=0.05, maturity=5, frequency=1, grace_years=2
):
    """
    Compara la estructura de flujos (cupones y principal) para distintos tipos de bonos:
      - Zero Cupón: No paga cupón; el principal se paga al vencimiento.
      - Bullet: Paga cupones periódicos; el principal se paga íntegro al final.
      - Amortizing: Se amortiza el principal en cada período de forma lineal.
      - Con Años de Gracia: No se pagan cupones durante 'grace_years';
          luego se pagan los cupones acumulados (se puede interpretar de distintas formas).

    Parámetros:
      - par: Valor nominal del bono.
      - coupon_rate: Tasa cupón anual.
      - maturity: Plazo total en años.
      - frequency: Número de pagos al año.
      - grace_years: Años sin pago (por simplicidad, sin cupones) para el bono con gracia.

    Retorna:
      - Un diccionario de DataFrames con el detalle de flujos para cada tipo.
    """
    n_periods = maturity * frequency
    period_times = np.arange(1, n_periods + 1)

    # Inicializar diccionario para almacenar DataFrames
    flows = {}

    # Zero Cupón: No hay cupones, el principal se paga al final.
    df_zero = pd.DataFrame(
        {
            "Periodo": period_times,
            "Cupón": [0] * n_periods,
            "Principal": [0] * (n_periods - 1) + [par],
        }
    )
    flows["Zero Cupón"] = df_zero

    # Bullet: Se pagan cupones fijos en cada período y el principal se paga al final.
    coupon_payment = par * coupon_rate / frequency
    df_bullet = pd.DataFrame(
        {
            "Periodo": period_times,
            "Cupón": [coupon_payment] * n_periods,
            "Principal": [0] * (n_periods - 1) + [par],
        }
    )
    flows["Bullet"] = df_bullet

    # Amortizing: Se paga una parte constante del principal en cada período.
    principal_payment = par / n_periods
    amortizing_cupones = []
    amortizing_principales = []
    outstanding = par
    for i in range(n_periods):
        cup = outstanding * coupon_rate / frequency
        amortizing_cupones.append(cup)
        amortizing_principales.append(principal_payment)
        outstanding -= principal_payment
    df_amortizing = pd.DataFrame(
        {
            "Periodo": period_times,
            "Cupón": amortizing_cupones,
            "Principal": amortizing_principales,
        }
    )
    flows["Amortizing"] = df_amortizing

    # Con Años de Gracia:
    # Se asume que durante los primeros 'grace_years' no se paga cupón ni principal,
    # y al finalizar el periodo de gracia se acumulan los cupones (por simplicidad, se pagan al final del período de gracia)
    # y luego se comporta como un bono bullet.
    n_grace_periods = grace_years * frequency
    df_grace = pd.DataFrame(
        {
            "Periodo": period_times,
            "Cupón": [0] * n_periods,
            "Principal": [0] * n_periods,
        }
    )
    # Durante la gracia: sin pagos
    # Desde el período n_grace_periods+1 hasta el final, se pagan cupones normales
    for i in range(n_grace_periods, n_periods):
        df_grace.loc[i, "Cupón"] = coupon_payment
    # Se paga el principal íntegro al final
    df_grace.loc[n_periods - 1, "Principal"] = par
    flows[f"Con {grace_years} Años de Gracia"] = df_grace

    # Mostrar cada DataFrame y graficar sus flujos acumulados
    for tipo, df in flows.items():
        print(f"\n--- {tipo} ---")
        print(df)

        # Graficar flujos acumulados: Cupón y Principal
        plt.figure(figsize=(8, 4))
        plt.bar(df["Periodo"] - 0.15, df["Cupón"], width=0.3, label="Cupón")
        plt.bar(df["Periodo"] + 0.15, df["Principal"], width=0.3, label="Principal")
        plt.xlabel("Periodo")
        plt.ylabel("Monto")
        plt.title(f"Flujos de {tipo}")
        plt.xticks(df["Periodo"])
        plt.legend()
        plt.grid(True)
        plt.show()

    return flows


# Ejecutar función de precio-yield
plot_price_yield_relationship(
    par=100,
    coupon_rate=0.06,
    maturity=30,
    frequency=1,
    yield_min=0.001,
    yield_max=0.10,
    num_points=200,
)

# Ejecutar función de comparación de flujos para distintos tipos de bonos
bond_flows = compare_bond_cash_flows(
    par=100, coupon_rate=0.05, maturity=5, frequency=1, grace_years=2
)


def calculate_bond_price_with_dates(
    coupon_rate,
    ytm,
    principal,
    valuation_date,
    day_convention=360,
    schedule_df=None,
    adjust_type='RiskAmerica',
):
    """
    Calcula el precio de un bono utilizando fechas reales y ajusta el factor de descuento
    de acuerdo con la siguiente fórmula para el exponente:

        exponente = (días desde valoración hasta pago / day_convention) + (extra_days / days_in_period)

    donde:
      - extra_days es la diferencia (si es positiva) entre la fecha real de pago y la fecha programada.
      - days_in_period es el número de días en el período de cupón (sin ajuste).

    Parámetros:
      - coupon_rate (float): Tasa cupón anual (ej. 0.06 para 6%).
      - ytm (float): Tasa de rendimiento exigida anual en forma decimal.
      - principal (float): Valor nominal del bono.
      - valuation_date (str o datetime): Fecha de valoración.
      - day_convention (int): Base de días para el descuento (ej. 360 para 30/360 o 365 para actual/365).
      - schedule_df (DataFrame): DataFrame con el calendario de pagos, con columnas:
            'period', 'date' (fecha programada) y 'payment date' (fecha real de pago).
      - adjust_for_bad_days (bool): Si es True, se incluye el ajuste extra de días de pago (true yield).

    Retorna:
      - price (float): Precio total del bono.
      - df (DataFrame): Detalle de cada flujo con columnas:
          'period', 'Scheduled_Date', 'Payment_Date', 'Días', 'Extra_Days', 'Days_in_Period',
          'Flujo', 'Factor_Descuento' y 'Valor_Presente'.
    """

    # Convertir valuation_date a datetime si es string
    if isinstance(valuation_date, str):
        valuation_date = pd.to_datetime(valuation_date, dayfirst=True)

    # Convertir las columnas de fecha a formato datetime
    for col in ["date", "payment date"]:
        schedule_df[col] = pd.to_datetime(
            schedule_df[col], dayfirst=True, errors="coerce"
        )

    # Ordenar el DataFrame por 'period'
    schedule_df = schedule_df.sort_values(by="period").reset_index(drop=True)

    # Calcular la columna "Days_in_Period" en base a la fecha programada.
    # Para el primer pago válido, se usa (scheduled_date - valuation_date).days;
    # para los siguientes, se usa la diferencia entre el scheduled_date actual y el anterior.
    days_in_period = []
    for idx, row in schedule_df.iterrows():
        sched_date = row["date"]
        if pd.isnull(sched_date):
            days_in_period.append(np.nan)
        else:
            if idx == 0:
                dpi = (sched_date - valuation_date).days
            else:
                prev_sched = schedule_df.loc[idx - 1, "date"]
                # Si la fila anterior no tiene fecha (por ejemplo, emisión), se usa valuation_date
                if pd.isnull(prev_sched):
                    dpi = (sched_date - valuation_date).days
                else:
                    dpi = (sched_date - prev_sched).days
            days_in_period.append(dpi)
    schedule_df["Days_in_Period"] = days_in_period

    # Filtrar solo los períodos que tengan 'payment date' definido
    schedule_df = schedule_df[schedule_df["payment date"].notnull()].reset_index(
        drop=True
    )

    # Se infiere la frecuencia (número de pagos al año) usando el promedio de "Days_in_Period"
    if len(schedule_df) > 0:
        avg_days = schedule_df["Days_in_Period"].mean()
        frequency = round(365 / avg_days) if avg_days > 0 else 1
    else:
        frequency = 1

    # Calcular el pago de cupón periódico
    coupon_payment = principal * coupon_rate / frequency
    
    days_next_coupon = abs((valuation_date - schedule_df.loc[0,'date']).days)
    
    days_first_period = schedule_df.loc[0,'Days_in_Period']

    data = []

    # Procesar cada período
    for idx, row in schedule_df.iterrows():
        period = row["period"]
        scheduled_date = row["date"]
        payment_date = row["payment date"]
        days_in_per = row["Days_in_Period"]
        
        # Solo considerar flujos a partir de la fecha de valoración
        if payment_date < valuation_date:
            continue

        # Días transcurridos desde la fecha de valoración hasta la fecha real de pago
        days = (payment_date - valuation_date).days

        # extra_days: Diferencia entre la fecha real de pago y la fecha programada
        extra_days = (
            max((payment_date - scheduled_date).days, 0)
            if pd.notnull(scheduled_date)
            else 0
        )
        
        if extra_days>0:
            
            logger.debug(f'Días extra en periodo {period}')

        # Calcular el exponente:
        
        if adjust_type =='BBG':
            #   parte 1:((days_next_coupon / day_convention)  + idx
            #   si es el actual 0 porque se captura en la parte izquierda y 
            #   luego se suma 1 añadiendo el denominador completo
            #   parte 2: extra_days / (days in period)
            exponent = ((days_next_coupon / (day_convention/frequency))  + int(idx)) + (extra_days / days_in_per )
        
        elif adjust_type == 'RiskAmerica':
            exponent = (days / days_first_period) 
        else:
            raise('Tipo de calculo no permitido. Seleccione ["BBG", "RiskAmerica"]')
            
        
        
        discount_factor = 1 / ((1 + (ytm/frequency)) ** exponent)

        # Flujo: en cada período se paga cupón; en el último, se suma el principal.
        cash_flow = coupon_payment
        if idx == schedule_df.index[-1]:
            cash_flow += principal

        present_value = cash_flow * discount_factor

        data.append(
            {
                "period": period,
                "Scheduled_Date": scheduled_date.strftime("%Y-%m-%d"),
                "Payment_Date": payment_date.strftime("%Y-%m-%d"),
                "Días": days,
                "Extra_Days": extra_days,
                "Days_in_Period": days_in_per,
                "Flujo": cash_flow,
                "Factor_Descuento": discount_factor,
                "Valor_Presente": present_value,
            }
        )

    df = pd.DataFrame(data)
    price = df["Valor_Presente"].sum()

    # Agregar fila total
    total_row = pd.DataFrame(
        [
            {
                "period": "Total",
                "Scheduled_Date": "",
                "Payment_Date": "",
                "Días": "",
                "Extra_Days": "",
                "Days_in_Period": "",
                "Flujo": df["Flujo"].sum(),
                "Factor_Descuento": "",
                "Valor_Presente": price,
            }
        ]
    )
    df = pd.concat([df, total_row], ignore_index=True)

    return price, df


# ----- Ejemplo de uso con la data proporcionada -----

# Primero veremos el ejemplo simplificado

face_value = 1000
maturity = 10
yield_rate = 0.06
coupon_rate = 0.06
price_of_bond(face_value, coupon_rate, maturity, yield_rate, frequency=2)

# Casi similar al principal np.float64(999.9999999999995) ya que el bono 
# transa a la par

# Ahora comparamos con el ejemplo con convencion y fechas efectivas de pago.

data_schedule = {
    "period": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "date": [
        "01-03-2025",
        "01-09-2025",
        "01-03-2026",
        "01-09-2026",
        "01-03-2027",
        "01-09-2027",
        "01-03-2028",
        "01-09-2028",
        "01-03-2029",
        "01-09-2029",
        "01-03-2030",
    ],
    "payment date": [
        None,
        "01-09-2025",
        "01-03-2026",
        "01-09-2026",
        "01-03-2027",
        "01-09-2027",
        "01-03-2028",
        "01-09-2028",
        "01-03-2029",
        "01-09-2029",
        "01-03-2030",
    ],
}

schedule_df = pd.DataFrame(data_schedule)

# Convertir las columnas de fecha
for col in ["date", "payment date"]:
    schedule_df[col] = pd.to_datetime(
        schedule_df[col], dayfirst=True, errors="coerce"
    )

# Parámetros del bono (ejemplo)
coupon_rate = 0.06  # 6% anual
ytm = 0.06  # 6% rendimiento exigido
principal = 1000  # Valor nominal
valuation_date = "01-03-2025"  # Fecha de valoración

price, bond_schedule_df = calculate_bond_price_with_dates(
    coupon_rate=coupon_rate,
    ytm=ytm,
    principal=principal,
    valuation_date=valuation_date,
    day_convention=365,
    schedule_df=schedule_df,
    adjust_type='RiskAmerica',  # Activa el ajuste de días malos
)

print("Precio del bono:", price)
print(bond_schedule_df)

