# Descripción del Proyecto

Este proyecto consiste en un sistema automatizado de backtesting cuantitativo para la gestión dinámica de portafolios de inversión basados en activos tecnológicos (CÉDEARs). El objetivo principal es evaluar el rendimiento de estrategias de Optimización de Media-Varianza (Markowitz), comparando modelos estáticos frente a modelos dinámicos con fricción operativa real.


# Contenido del Reporte

El reporte generado sistematiza el desempeño durante el período 2025 y se divide en cuatro ejes fundamentales:

I. Atribución de Performance y Eficiencia (KPIs)

    Comparativa: Evalúa tres estrategias: Equitativa (1/N), Markowitz Estático y Markowitz Dinámico (Inviu).

    Métricas de Riesgo: Incluye Sharpe Ratio, Sortino, Maximum Drawdown (MDD) y el Ratio Calmar, permitiendo entender no solo cuánto se ganó, sino a qué costo de volatilidad y dolor (drawdown).

II. Auditoría de Fricción y Costos Operativos (Turnover)

    Analiza el impacto real de las comisiones del bróker sobre el rendimiento bruto.

    Cuantifica el Turnover (volumen nominal operado), permitiendo identificar cuánto capital se pierde en aranceles e impuestos (IVA) debido a la frecuencia de rebalanceo.

III. Matriz de Retornos Mensuales Comparativa

    Un desglose cronológico mes a mes de los retornos logarítmicos, facilitando la identificación de períodos de crisis (ej. marzo 2025) y recuperación de mercado.

IV. Evolución y Alocación de Activos

    Evolución del Capital: Gráfico comparativo de la curva de valor liquidativo (NAV) de las tres estrategias sobre un capital inicial de USD 10.000.

    Historial de Pesos: Una tabla detallada que muestra cómo el algoritmo ajustó la exposición a activos (AAPL, MSFT, GOOGL, AMZN, NVDA, META) mes a mes, aplicando filtros de regularización para evitar la rotación excesiva.

# Consideraciones Técnicas

    Regularización: El modelo incorpora un factor de inercia (freno de mano) que penaliza la rotación innecesaria, optimizando el Net Sharpe Ratio al reducir el costo de transacción.

    Limitaciones: La estrategia utiliza una ventana móvil de 365 días para el entrenamiento de los modelos y rebalanceo mensual sistemático.