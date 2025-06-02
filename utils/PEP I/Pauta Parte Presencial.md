## PEP I


--- 


**1. Preguntas de Desarrollo (60%)**

### 1. Preguntas de Desarrollo (60%)

**a. Defina qué es un bono incluyendo la clasificación en cuanto a la estructura de capitalización del instrumento.**

Un **bono** es un título de deuda emitido por una entidad (gobierno, empresa o institución) que se compromete a pagar al tenedor:

1. **El valor nominal** (o principal) en la fecha de vencimiento.
2. **Flujos periódicos** de intereses (cupones) a una tasa preestablecida.

La clasificación de un bono según la **estructura de capitalización de los intereses** se basa en cómo y cuándo se incorporan los cupones al capital:

* **Bono cupón cero (zero-coupon bond)**
  — No paga cupones periódicos: todo el rendimiento se capitaliza y se recibe al vencimiento.
  — Se emite con descuento sobre el valor nominal.
  — Equivalencia: tasa de interés efectiva.
  — Fondo teórico: la fórmula de valoración es

  $$
  P = \frac{F}{(1 + y)^n}
  $$

  donde $P$ es el precio, $F$ el valor nominal, $y$ la tasa efectiva y $n$ los períodos hasta vencimiento (Fabozzi, 2016).

* **Bono Bullet**
  — El interés se paga según un cronograma (anual, semestral, trimestral…).
  — Valoración mediante suma de valor presente de cada cupón y del principal:

  $$
  P = \sum_{t=1}^n \frac{C}{(1 + y_t)^t} + \frac{F}{(1 + y_n)^n}
  $$

  donde $C$ es el cupón periódico y $y_t$ la tasa al período $t$.


* **Bono amortizable**
  — Combina pago de intereses y amortización gradual del principal.
  — Impacta en la estructura de flujos y, por tanto, en duración y convexidad.


**b. Considerando un alza de 100 puntos base en la tasa de mercado. ¿Qué debiera hacer con las medidas de riesgo (duración, convexidad) para estimar el precio del instrumento? Explique con sus palabras.**

Cuando la tasa de mercado aumenta 100 pb ($\Delta y = +1\%$), las **medidas de riesgo** usadas para aproximar el cambio en precio $\Delta P$ son:

1. **Duración modificada** $\mathrm{D_{mod}}$
   — Define la sensibilidad lineal del precio:

   $$
   \frac{\Delta P}{P} \approx -\mathrm{D_{mod}}\;\Delta y
   $$

   — Depende inversamente de la tasa: al cambiar $y$, $\mathrm{D_{mod}}$ también varía.

2. **Convexidad** $C$
   — Captura la curvatura de la relación precio–tasa:

   $$
   \frac{\Delta P}{P} \approx -\mathrm{D_{mod}}\;\Delta y + \tfrac{1}{2}C\;(\Delta y)^2
   $$

   — También es función de $y$ y de los plazos de los flujos.

**Clave para estimar precios tras un gran cambio de tasa**

* **Recalcular** $\mathrm{D_{mod}}$ y $C$ en el nuevo nivel de rendimiento “intermedio” (por ejemplo, en $y + \tfrac{1}{2}\Delta y$) para mejorar la aproximación.
* Si el cambio es muy grande, **usar valoración exacta** descontando todos los flujos con la nueva curva de rendimientos.

Este enfoque garantiza que las medidas, que son derivadas de precio respecto a la tasa, reflejen la dependencia no lineal real de los bonos (Tuckman & Serrat, 2012).


**c. Una empresa de importación chilena que vende Bourbon a supermercados y distribuidoras a nivel local, lo contrata a usted para asesorar al Gerente de Finanzas respecto al uso de derivados para generar cobertura de tipo de cambio respecto a su deuda de 1.000.000 USD a 1 año. Si el precio del dólar spot es 1000, el precio Forward a 1 año es 1100, la tasa de interés en CLP del período es 5% y la tasa de interés en USD es de 4%. Explique con sus palabras qué le recomendaría al importador.**


* **Spot actual:** $S = 1000$ CLP/USD
* **Forward 1 año:** $F = 1100$ CLP/USD
* **Tasa CLP (dom.):** $r_d = 5\%$
* **Tasa USD (for.):** $r_f = 4\%$

Según la **paridad de tasas de interés** (no existe arbitraje),

$$
F^* = S \times \frac{1 + r_d}{1 + r_f} 
     = 1000 \times \frac{1{,}05}{1{,}04} 
     \approx 1009{,}62\;\text{CLP/USD}.
$$

Como el forward de mercado (1100) es > $F^*$, está **sobrevaluado** respecto al arbitraje.

**Recomendación de cobertura:**

1. **Cobertura con mercado de dinero (money market hedge):**

   * *Paso 1:* Pedir prestado en CLP.
   * *Paso 2:* Comprar USD e invertirlos a $r_{usd}$.
   * *Paso 3:* Pagar deuda con USD y con ingresos en peso pagar deuda inicial.

2. **Arbitraje**
   

**Conclusión:** usar la **cobertura de mercado de dinero**, ya que el forward cotiza por encima del nivel teórico de paridad y resulta más caro al vencimiento (Hull, 2018).


**d. Uno de los directores plantea que es posible vender un bono a 3 años a una tasa de 6,05% para recaudar más y usted sabe que actualmente el bono libre de riesgo en pesos a 3 años transa en 6,10%. ¿Qué opina de la tasa a la que quiere colocar el director?**


* El mercado de bonos soberanos a 3 años (riesgo cero) rinde **6,10%**.
* El director quiere emitir a **6,05%**, es decir, **5 pb** por debajo del libre de riesgo.

**Opinión:**

* Un bono corporativo debería ofrecer, en principio, una **prima de riesgo** sobre el soberano (cupones más altos) para compensar riesgo de crédito y liquidez.
* Si se coloca a una tasa menor que el soberano,

  1. **No resulta atractivo** para inversores racionales: preferirían tomar el activo libre de riesgo.
  2. Puede interpretarse como **subcotización** o indicador de **error en pricing**.
  3. Implicaría financiación “demasiado barata” para la empresa, pero difícil de colocar.

Por tanto, **la tasa de 6,05% es inadecuada**: debería estar al menos en 6,10% + spread de crédito (Fabozzi, 2016).

---




### 2. Comente la veracidad, falsedad o incertidumbre de las siguientes afirmaciones: (40%)

a. Utilizando la convexidad en lugar de la duración modificada se obtiene una aproximación más precisa del cambio porcentual del precio de un bono cuando cambia su TIR.

b. En un bono corporativo amortizable, el riesgo de crédito afecta principalmente el retorno total si el emisor falla en cumplir con el pago de los cupones, pero el riesgo de reinversión no es relevante.

c. La duración Macaulay de un bono cero cupón (Zero) corresponde a su madurez.

d. Una curva de tasas de interés con pendiente negativa generalmente indica expectativas de expansión económica e inflación.


| Afirmación                                                                                                                                                     | Veredicto     | Justificación clave                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| a) Usar convexidad en lugar de duración modificada ofrece una aproximación más precisa del cambio porcentual del precio ante variaciones de TIR.               | **Verdadero** | La duración linealiza el cambio; la convexidad corrige la curvatura. Para $\Delta y$ grandes, añadir $\tfrac12C(\Delta y)^2$ reduce el error de aproximación (Tuckman & Serrat, 2012).                          |
| b) En un bono corporativo amortizable, el riesgo de crédito impacta total return si el emisor incumple cupones, pero el riesgo de reinversión no es relevante. | **Falso**     | En amortizables, los pagos de principal y cupón intermedios requieren reinversión a tasas inciertas: el riesgo de reinversión sí afecta el rendimiento efectivo total (Fabozzi, 2016).                          |
| c) La duración de Macaulay de un bono cupón cero (Zero) corresponde a su madurez.                                                                              | **Verdadero** | Al no haber pagos intermedios, el único flujo es al vencimiento $n$; la duración Macaulay = $\sum t\frac{PV_t}{P} = n$.                                                                                         |
| d) Una curva de tasas con pendiente negativa indica generalmente expectativas de expansión económica e inflación.                                              | **Falso**     | Una pendiente negativa suele anticipar **recesión** o menor inflación futura, pues el mercado espera que las tasas bajen (yield curve inversion es signo de enfriamiento económico) (Estrella & Mishkin, 1998). |

---

**Bibliografía**

* Fabozzi, F. J. (2016). *THE HANDBOOK OF FIXED INCOME SECURITIES*. Pearson.
* CFA. Fixed Income Analysis.
* Hull, J. C. (2018). *INTRODUCCIÓN A LOS MERCADOS DE FUTUROS Y OPCIONES* (10ª ed.). Pearson.
* Tuckman, B., & Serrat, A. (2012). Fixed Income Securities: Tools for Today’s Markets (3ª ed.). Wiley.
