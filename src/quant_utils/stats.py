# src/quant-utils/stats.py

import numpy as np
import pandas as pd

class FinancialStats:
    """Clase encargada de procesar datos y calcular métricas estadísticas financieras."""

    @staticmethod
    def calcular_retornos_log(precios: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula los retornos logarítmicos continuos a partir de un DataFrame de precios.
        R_t = ln(P_t / P_{t-1})
        """
        # Aseguramos trabajar con precios ordenados cronológicamente
        precios_ordenados = precios.sort_index()
        retornos = np.log(precios_ordenados / precios_ordenados.shift(1))
        return retornos.dropna()

    @staticmethod
    def matriz_covarianza(retornos: pd.DataFrame, periodos_ano: int = 252) -> pd.DataFrame:
        """
        Calcula y anualiza la matriz de covarianza muestral de los retornos.
        """
        return retornos.cov() * periodos_ano

    @staticmethod
    def metricas_portafolio(pesos: np.ndarray, 
                            retornos: pd.DataFrame, 
                            periodos_ano: int = 252) -> tuple[float, float]:
        """
        Calcula el retorno esperado y la volatilidad anualizada de un portafolio.
        
        Retorna:
            tuple[float, float]: (Retorno esperado, Volatilidad del portafolio)
        """
        # Normalizar pesos por seguridad para que sumen 1
        pesos = pesos / np.sum(pesos)
        
        # Retornos esperados anualizados de cada activo (media aritmética)
        retornos_medios = retornos.mean() * periodos_ano
        retorno_portafolio = float(np.dot(pesos, retornos_medios))
        
        # Riesgo (Volatilidad) utilizando la forma cuadrática: sqrt(w^T * Sigma * w)
        sigma = FinancialStats.matriz_covarianza(retornos, periodos_ano).values
        varianza_portafolio = np.dot(pesos.T, np.dot(sigma, pesos))
        volatilidad_portafolio = float(np.sqrt(varianza_portafolio))
        
        return retorno_portafolio, volatilidad_portafolio

    @staticmethod
    def calcular_var_historico(retornos_portafolio: pd.Series, nivel_confianza: float = 0.95) -> float:
        """
        Calcula el Value at Risk (VaR) Histórico no paramétrico del portafolio.
        Representa la máxima pérdida esperada dado un nivel de confianza.
        """
        # El percentil calcula el punto de corte en la cola izquierda de la distribución
        percentil = 1.0 - nivel_confianza
        var = np.percentile(retornos_portafolio, percentil * 100)
        return float(var)