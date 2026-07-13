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
        precios_ordenados = precios.sort_index()
        return np.log(precios_ordenados / precios_ordenados.shift(1)).dropna()
        
    
    @staticmethod
    def get_var_historico(retornos_portafolio: pd.Series, nivel_confianza: float = 0.95) -> float:
        """
        Calcula el Value at Risk (VaR) Histórico no paramétrico del portafolio.
        Representa la máxima pérdida esperada dado un nivel de confianza.
        """
        # El percentil calcula el punto de corte en la cola izquierda de la distribución
        percentil = 1.0 - nivel_confianza
        var = np.percentile(retornos_portafolio, percentil * 100)
        return float(var)
    
    @staticmethod
    def get_max_drawdown(retornos: pd.Series) -> float:
        """
        Calcula la máxima pérdida consecutiva desde el pico más alto (Peak-to-Trough).
        Devuelve el valor en formato decimal (ej: 0.15 para un -15%).
        """
        cum_ret = (1 + retornos).cumprod()
        peak = cum_ret.cummax()
        drawdowns = (retornos - peak) / peak
        return drawdowns.min() # Lo devolvemos positivo por convención financiera

    @staticmethod
    def get_ratio_calmar(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """
        Calcula el Ratio de Calmar: Retorno Anualizado / Maximum Drawdown.
        Mide cuánto retorno te da el algoritmo por cada unidad de dolor (caída máxima).
        """
        max_dd = FinancialStats.get_max_drawdown(curva_equidad)
        
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
    def get_anual_volatility(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """Calcula la desviación estándar anualizada de los retornos diarios."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        return retornos_diarios.std() * np.sqrt(dias_anualizacion)

    @staticmethod
    def get_ratio_sharpe(curva_equidad: pd.Series, risk_free_rate: float = 0.0, dias_anualizacion: int = 252) -> float:
        """Calcula el Ratio de Sharpe Anualizado."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        exceso_retornos = retornos_diarios - (risk_free_rate / dias_anualizacion)
        
        if exceso_retornos.std() == 0:
            return np.nan
            
        return (exceso_retornos.mean() / exceso_retornos.std()) * np.sqrt(dias_anualizacion)

    @staticmethod
    def get_ratio_sortino(curva_equidad: pd.Series, risk_free_rate: float = 0.0, dias_anualizacion: int = 252) -> float:
        """Calcula el Ratio de Sortino Anualizado (solo penaliza volatilidad negativa)."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        exceso_retornos = retornos_diarios - (risk_free_rate / dias_anualizacion)
        
        # Filtrar solo los días con retornos negativos para calcular la baja desviación estándar
        retornos_negativos = exceso_retornos[exceso_retornos < 0]
        downside_std = retornos_negativos.std()
        
        if downside_std == 0 or np.isnan(downside_std):
            return np.nan
            
        return (exceso_retornos.mean() / downside_std) * np.sqrt(dias_anualizacion)
    

    @staticmethod
    def get_risk_metrics(retornos: pd.Series, rf: float = 0.0) -> dict:
        """Métricas estándar de riesgo."""
        
        sharpe = FinancialStats.get_ratio_sharpe(retornos, rf)
        mdd = FinancialStats.get_max_drawdown(retornos)
        
        return {"sharpe": sharpe, "mdd": mdd}