
# Escalabilidad

Si el día de mañana quisieras escalar tu bot para optimizar 500 o 1000 acciones a la vez, el código de tu librería tendría que evolucionar en la carpeta src/quant_utils/ incorporando estas soluciones avanzadas:

    Modelos de Factores (Reducción de Dimensionalidad): En lugar de hacer una matriz de 500x500, usás álgebra lineal (como PCA - Principal Component Analysis) para reducir el problema a 5 factores de riesgo principales.

    Shrinkage (Ledoit-Wolf): Aplicar algoritmos que "suavizan" matemáticamente la matriz de covarianza antes de pasársela al optimizador para eliminar el ruido numérico.

    Optimización Convexa Especializada: Dejar de usar el minimize genérico de SciPy y pasar a usar librerías específicas de optimización financiera como cvxpy, que resuelven problemas de miles de variables en microsegundos porque usan solvers específicos para formas cuadráticas.