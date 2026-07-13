# Teoría de Portafolio de Harry Markowitz (1952)

El núcleo de la Modern Portfolio Theory (MPT) es demostrar matemáticamente que **el riesgo de un portafolio no es la suma de los riesgos de sus activos individuales**, sino que depende crucialmente de la **correlación** entre ellos.

## 1. El Retorno Esperado del Portafolio ($E[R_p]$)
Es simplemente una combinación lineal (promedio ponderado) de los retornos esperados de cada activo:

$$E[R_p] = \sum_{i=1}^{N} w_i E[R_i] = w^T E[R]$$

Donde:
- $w$ es el vector columna de pesos ($N \times 1$).
- $E[R]$ es el vector columna de retornos esperados ($N \times 1$).

## 2. El Riesgo (Varianza) del Portafolio ($\sigma^2_p$)
Aquí ocurre la magia de la diversificación. Para un portafolio de 2 activos, la varianza es:

$$\sigma^2_p = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_{1,2}$$

Donde $\sigma_{1,2}$ es la **covarianza**. Si la covarianza es negativa, el tercer término *resta* riesgo al total.

Expresado de forma matricial para $N$ activos (reducción dimensional):

$$\sigma^2_p = w^T \Sigma w$$

Donde $\Sigma$ es la Matriz de Covarianza ($N \times N$).

## 3. El Problema de Optimización Matemática
Para encontrar la **Frontera Eficiente**, Markowitz plantea un problema de optimización cuadrática con restricciones lineales:

$$\min_{w} \quad \frac{1}{2} w^T \Sigma w$$

**Sujeto a:**
1. $\sum_{i=1}^N w_i = 1$ (Restricción de capital: usar todo el dinero).
2. $w_i \ge 0$ (Restricción de no ventas en corto o *long-only*).
3. $w^T E[R] = R_{target}$ (Alcanzar un retorno objetivo específico).