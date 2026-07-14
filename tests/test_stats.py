# tests/test_stats.py

import numpy as np
import pandas as pd
import pytest
from quant_utils import FinancialStats

@pytest.fixture
def datos_precios_fijos():
    """Fixture que genera un DataFrame de precios fijos para los tests."""
    fechas = pd.date_range(start="2026-01-01", periods=4, freq="D")
    # Precios que suben de forma constante y predecible
    # Retornos logarítmicos individuales van a ser ln(2) = 0.693147
    data = {
        'Activo_A': [10.0, 20.0, 40.0, 80.0],
        'Activo_B': [10.0, 20.0, 40.0, 80.0]
    }
    return pd.DataFrame(data, index=fechas)

def test_calcular_retornos_log(datos_precios_fijos):
    retornos = FinancialStats.calcular_retornos_log(datos_precios_fijos)
    
    # El tamaño del df de retornos debe ser N-1
    assert len(retornos) == 3
    # El retorno logarítmico de 10 a 20 es ln(2) ≈ 0.6931
    assert pytest.approx(retornos.iloc[0, 0], 0.0001) == 0.693147
