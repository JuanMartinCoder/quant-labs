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
    
    @staticmethod
    def calcular_maximum_drawdown(curva_equidad: pd.Series) -> float:
        """
        Calcula la máxima pérdida consecutiva desde el pico más alto (Peak-to-Trough).
        Devuelve el valor en formato decimal (ej: 0.15 para un -15%).
        """
        # 1. Calculamos el pico máximo acumulado hasta cada día
        picos = curva_equidad.cummax()
        
        # 2. Calculamos la caída porcentual desde ese pico histórico diario
        drawdowns = (curva_equidad - picos) / picos
        
        # 3. Nos quedamos con la caída más profunda (el mínimo de la serie)
        max_drawdown = drawdowns.min()
        
        return abs(max_drawdown) # Lo devolvemos positivo por convención financiera

    @staticmethod
    def calcular_ratio_calmar(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """
        Calcula el Ratio de Calmar: Retorno Anualizado / Maximum Drawdown.
        Mide cuánto retorno te da el algoritmo por cada unidad de dolor (caída máxima).
        """
        max_dd = FinancialStats.calcular_maximum_drawdown(curva_equidad)
        
        if max_dd == 0:
            return np.nan
            
        # Calcular Retorno Total Bruto
        retorno_total = curva_equidad.iloc[-1] - 1
        
        # Anualizar el retorno basado en la cantidad de días de la serie
        n_dias = len(curva_equidad)
        anios = n_dias / dias_anualizacion
        retorno_anualizado = (retorno_total + 1) ** (1 / anios) - 1
        
        return retorno_anualizado / max_dd
    
    @staticmethod
    def calcular_volatilidad_anualizada(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """Calcula la desviación estándar anualizada de los retornos diarios."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        return retornos_diarios.std() * np.sqrt(dias_anualizacion)

    @staticmethod
    def calcular_ratio_sharpe(curva_equidad: pd.Series, risk_free_rate: float = 0.0, dias_anualizacion: int = 252) -> float:
        """Calcula el Ratio de Sharpe Anualizado."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        exceso_retornos = retornos_diarios - (risk_free_rate / dias_anualizacion)
        
        if exceso_retornos.std() == 0:
            return np.nan
            
        return (exceso_retornos.mean() / exceso_retornos.std()) * np.sqrt(dias_anualizacion)

    @staticmethod
    def calcular_ratio_sortino(curva_equidad: pd.Series, risk_free_rate: float = 0.0, dias_anualizacion: int = 252) -> float:
        """Calcula el Ratio de Sortino Anualizado (solo penaliza volatilidad negativa)."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        exceso_retornos = retornos_diarios - (risk_free_rate / dias_anualizacion)
        
        # Filtrar solo los días con retornos negativos para calcular la baja desviación estándar
        retornos_negativos = exceso_retornos[exceso_retornos < 0]
        downside_std = retornos_negativos.std()
        
        if downside_std == 0 or np.isnan(downside_std):
            return np.nan
            
        return (exceso_retornos.mean() / downside_std) * np.sqrt(dias_anualizacion)