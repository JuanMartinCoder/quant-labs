# Quant-Lab 📊📈

Un entorno integral de desarrollo, experimentación y backtesting para **Finanzas Cuantitativas**. Este repositorio funciona como un laboratorio personal modularizado para la simulación de estrategias, optimización de portafolios bajo la teoría de Markowitz, análisis avanzado de riesgo y generación automatizada de reportes institucionales.

---

## 🚀 Objetivos del Proyecto

*   **Sandbox de Investigación:** Espacio dedicado a prototipar ideas de inversión y analizar teorías financieras (ej. Fronteras eficientes de Markowitz).
*   **Motor de Backtesting:** Simulación y validación de estrategias sistemáticas con tracking detallado frente a benchmarks sectoriales (ej. Invesco QQQ).
*   **Cálculo de Riesgo Avanzado:** Implementación estadística de métricas de atribución de performance, volatilidad y preservación de capital.
*   **Pipeline Automatizado de Reportes:** Generación de documentos ejecutivos en formato PDF con diseño institucional a partir de plantillas HTML dinámicas.

---

## 📂 Estructura del Repositorio

El laboratorio está organizado bajo estándares profesionales de desarrollo de software (Data-Science/Quant layout):

```text
.
├── pyproject.toml                 # Configuración del proyecto y definición de dependencias
├── uv.lock                        # Archivo de bloqueo de dependencias (gestionado por uv)
├── data/                          # Ciclo de vida de los datos financieros
│   ├── raw/                       # Datos crudos históricos (precios.parquet, benchmark_QQQ.csv)
│   ├── processed/                 # Datos transformados listos para análisis
│   └── interim/                   # Artefactos visuales intermedios (equity_curve.png, asset_allocation.png)
├── notebooks/                     # Flujos de trabajo experimentales y prototipado
│   ├── 01_backtesting/            # Notebooks de desarrollo de estrategias
│   ├── 02_risk_analysis/          # Notebooks de análisis de métricas de riesgo
│   └── research/                  # Carpetas de investigación específica (Markowitz, históricos 2024-2025)
├── src/
│   └── quant_utils/               # Librería interna del laboratorio (Modular y reutilizable)
│       ├── data_downloader.py     # Ingesta y descargas automatizadas de APIs
│       ├── data_manager.py        # Limpieza, parseo y persistencia de series temporales
│       ├── optimization.py        # Algoritmos de optimización de carteras y pesos mínimos
│       ├── stats.py               # Motor matemático: Sharpe, Sortino, Alfas, Betas y Drawdowns
│       ├── brokers.py             # Abstracciones para lógica de ejecución o simulación de órdenes
│       ├── templates/             # Plantillas base (report_template.html) para reportes visuales
│       └── reports/               # Componentes del motor de reporte (styles, plotting, generators)
└── tests/                         # Cobertura de tests unitarios (optimization, pipeline, stats)
```

## 🛠️ Stack Tecnológico y Entorno

El ecosistema de desarrollo y dependencias está administrado de forma unificada por **uv**, garantizando un entorno reproducible, rápido y aislado.

*   **Gestión de Entorno y Paquetes:** `uv` (configurado mediante `pyproject.toml` y congelado en `uv.lock`).
*   **Procesamiento Numérico y Datos:**
    *   `pandas` (Estructuración de dataframes y manipulación de series temporales).
    *   `numpy` / `scipy` (Cálculo matricial y optimizaciones estadísticas).
    *   `pyarrow` (Soporte de alta performance para la lectura y escritura del archivo de precios en formato `.parquet`).
*   **Visualización de Datos:** `matplotlib` y `seaborn` (Generación de gráficos de curvas de equidad y asignación de activos).
*   **Orquestador de Reportes:** 
    *   `jinja2` (Inyección dinámica de variables numéricas y gráficos en plantillas).
    *   `weasyprint` (Compilación y renderizado de HTML/CSS hacia documentos PDF con calidad de impresión A4).
*   **Testing y Calidad de Código:** `pytest` (Automatización y validación de las funciones de la librería interna).


## 🧬 Componentes del Núcleo (`src/quant_utils/`)

El core funcional del laboratorio está dividido en submódulos desacoplados:

1. **`stats.py`**: Calcula los indicadores de riesgo analizados en nuestro marco metodológico (Sharpe ajustado, Sortino con *downside deviation*, Alfa de Jensen, Beta de mercado y Máximo Drawdown intertemporal).
2. **`optimization.py`**: Modelado matemático de fronteras eficientes, maximización de ratios de eficiencia y matrices de covarianza de activos.
3. **`reports/`**: Módulo especializado que toma los resultados estadísticos de `stats.py`, genera los gráficos de curvas de equidad y distribución de activos en `data/interim/`, y los inyecta en `templates/report_template.html` utilizando tecnologías web (CSS adaptado a hojas A4) para compilar PDFs profesionales.

---

## 📦 Instalación y Uso de Laboratorio

Este proyecto utiliza `uv`. Si aún no lo tenés instalado en tu sistema, podés hacerlo siguiendo la documentación oficial de la herramienta.

### 1. Inicializar el entorno e instalar dependencias
Al clonar el repositorio, simplemente ejecutá el siguiente comando para que `uv` cree el entorno virtual sincrónico basado en el archivo `uv.lock`:

```bash
uv sync
```

### 2. Ejecutar los tests unitarios
Antes de correr backtests complejos, podés verificar la integridad matemática y de carga del pipeline ejecutando pytest:

```Bash
uv run pytest -v
```

### 3. Flujo de trabajo típico en Notebooks

Para empezar a experimentar en las carpetas de `notebooks/`, podés levantar tu servidor de Jupyter o interactuar directamente desde tu IDE activando el entorno virtual generado en `.venv/`. La librería `quant_utils` es totalmente importable desde cualquier subcarpeta de investigación:

```Python
from src.quant_utils.stats import get_risk_metrics
from src.quant_utils.optimization import get_max_sharpe

# Resto del codigo cuantitativo acá...
```

