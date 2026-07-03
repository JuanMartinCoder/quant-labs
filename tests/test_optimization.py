# tests/test_optimization.py

import numpy as np
import pandas as pd
import pytest
from quant_utils import FinancialStats, PortfolioOptimizer

@pytest.fixture
def datos_mercado_test():
    """
    Genera retornos para tres activos con comportamientos muy marcados,
    pero con escalas anualizadas lógicas del mercado real.
    """
    np.random.seed(42)
    fechas = pd.date_range(start="2026-01-01", periods=252, freq="B")
    
    # Retornos diarios realistas (Anualizados serían ~15%, ~2% y ~-10%)
    excelente = np.random.normal(0.0006, 0.01, 252)  
    estable = np.random.normal(0.0001, 0.001, 252) 
    malo = np.random.normal(-0.0004, 0.02, 252)    
    
    df_retornos = pd.DataFrame({
        'Excelente': excelente,
        'Estable': estable,
        'Malo': malo
    }, index=fechas)
    
    return df_retornos

# ==========================================
# TESTS DE RIESGO AVANZADO (FinancialStats)
# ==========================================

def test_calcular_var_historico():
    # Usamos una muestra lineal fija de retornos de portafolio para validar el percentil
    retornos_p = pd.Series(np.linspace(-0.10, 0.05, 101)) 
    var_95 = FinancialStats.calcular_var_historico(retornos_p, nivel_confianza=0.95)
    
    assert var_95 < 0
    # El percentil 5 en una lista ordenada de 101 puntos de -0.10 a 0.05 es exactamente -0.0925
    assert pytest.approx(var_95, 0.0001) == -0.0925


# ==========================================
# TESTS DE OPTIMIZACIÓN (PortfolioOptimizer)
# ==========================================

def test_max_sharpe_logica_financiera(datos_mercado_test):
    pesos = PortfolioOptimizer.max_sharpe(datos_mercado_test, tasa_libre_riesgo=0.0)
    
    # 1. Los pesos deben sumar 1
    assert pytest.approx(np.sum(pesos), 0.00001) == 1.0
    
    # 2. Ningún peso puede ser significativamente menor a cero
    assert np.all(pesos >= -1e-6) 
    
    # 3. El activo Malo debe tener una ponderación casi nula en comparación al Excelente
    assert pesos[2] < pesos[0]
    assert pesos[2] < 0.05


def test_minima_volatilidad_logica_financiera(datos_mercado_test):
    pesos = PortfolioOptimizer.minima_volatilidad(datos_mercado_test)
    
    assert pytest.approx(np.sum(pesos), 0.00001) == 1.0
    # La mayor porción de la torta tiene que ir obligatoriamente al activo Estable (índice 1)
    assert pesos[1] > pesos[0]
    assert pesos[1] > pesos[2]
    assert pesos[1] > 0.70


def test_optimizadores_limites_estrictos():
    """
    Valida límites estrictos usando ruido blanco aleatorio para evitar varianza cero,
    pero forzando un sesgo masivo en los retornos.
    """
    np.random.seed(42)
    fechas = pd.date_range(start="2026-01-01", periods=50, freq="D")
    
    # Agregamos una volatilidad mínima para que la matriz de covarianza sea invertible y válida
    ruido_normal = np.random.normal(0, 0.001, 50)
    ruido_absurdo = np.random.normal(0, 0.001, 50)
    
    df_absurdo = pd.DataFrame({
        'Normal': 0.001 + ruido_normal,
        'Absurdo': 0.5 + ruido_absurdo  # Retorno diario descomunal del 50%
    }, index=fechas)
    
    pesos = PortfolioOptimizer.max_sharpe(df_absurdo)
    
    # Comprobamos las restricciones del optimizador de SciPy
    assert pytest.approx(np.sum(pesos), 0.00001) == 1.0
    assert pesos[1] <= 1.00001
    assert pesos[0] >= -1e-6