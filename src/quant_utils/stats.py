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
    def get_max_drawdown(curva_equidad: pd.Series) -> float:
        """
        Calcula la máxima pérdida consecutiva desde el pico más alto (Peak-to-Trough).
        Devuelve el valor en formato decimal (ej: 0.15 para un -15%).
        """
        # 1. Limpieza absoluta de la serie antes de calcular picos
        curva_limpia = curva_equidad.dropna()
        curva_limpia = curva_limpia[curva_limpia > 0]  # El patrimonio nunca puede ser cero o menor
        
        if curva_limpia.empty:
            return 0.0

        # 2. Calcular picos históricos acumulados
        peak = curva_limpia.cummax()
        
        # 3. Calcular la serie de caídas respecto al pico actual
        drawdowns = (curva_limpia - peak) / peak
        
        return float(drawdowns.min()) # Lo devolvemos positivo por convención financiera

    @staticmethod
    def get_ratio_calmar(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """
        Calcula el Ratio de Calmar: Retorno Anualizado / Maximum Drawdown.
        Mide cuánto retorno te da el algoritmo por cada unidad de dolor (caída máxima).
        """
        max_dd = FinancialStats.get_max_drawdown(curva_equidad)
        
        if max_dd == 0 or np.isnan(max_dd):
            return np.nan
            
        # Calcular Retorno Total Bruto
        retorno_total = curva_equidad.iloc[-1] - 1
        
        # Anualizar el retorno basado en la cantidad de días de la serie
        n_dias = len(curva_equidad)
        anios = n_dias / dias_anualizacion
        retorno_anualizado = (retorno_total + 1) ** (1 / anios) - 1
        
        return float(retorno_anualizado / abs(max_dd))
    
    @staticmethod
    def get_anual_volatility(curva_equidad: pd.Series, dias_anualizacion: int = 252) -> float:
        """Calcula la desviación estándar anualizada de los retornos diarios."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        return float(retornos_diarios.std() * np.sqrt(dias_anualizacion))

    @staticmethod
    def get_ratio_sharpe(curva_equidad: pd.Series, risk_free_rate: float = 0.0, dias_anualizacion: int = 252) -> float:
        """Calcula el Ratio de Sharpe Anualizado."""
        retornos_diarios = curva_equidad.pct_change().dropna()
        exceso_retornos = retornos_diarios - (risk_free_rate / dias_anualizacion)
        
        if exceso_retornos.std() == 0:
            return np.nan
            
        return float((exceso_retornos.mean() / exceso_retornos.std()) * np.sqrt(dias_anualizacion))

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
            
        return float((exceso_retornos.mean() / downside_std) * np.sqrt(dias_anualizacion))
    

    @staticmethod
    def get_risk_metrics(retornos_portafolio: pd.Series, rf: float = 0.0) -> dict:
        """
        Genera el compendio de KPIs requerido para la tabla principal del reporte.
        """
        # Anualización estándar (252 días hábiles)
        retorno_anualizado = retornos_portafolio.mean() * 252
        volatilidad_anualizada = retornos_portafolio.std() * np.sqrt(252)
        
        # Sharpe Ratio
        sharpe = FinancialStats.get_ratio_sharpe(retornos_portafolio, rf)
        
        # Sortino Ratio (Penaliza solo volatilidad a la baja)
        sortino = FinancialStats.get_ratio_sortino(retornos_portafolio, rf)
        
        # Máximo Drawdown (MDD)
        max_dd = FinancialStats.get_max_drawdown(retornos_portafolio)
        
        # Calmar Ratio
        calmar = FinancialStats.get_ratio_calmar(retornos_portafolio)
        
        return {
            "retorno": retorno_anualizado,
            "volatilidad": volatilidad_anualizada,
            "sharpe": sharpe,
            "sortino": sortino,
            "max_dd": max_dd,
            "calmar": calmar
        }
    
    @staticmethod
    def get_monthly_matrix(retornos_diarios: pd.Series) -> pd.DataFrame:
        """
        Transforma una serie temporal de retornos diarios en la matriz mensual 
        agrupada por año y mes que exige el reporte visual.
        """
        # Resamplear a retornos mensuales compuestos
        resampled = retornos_diarios.groupby([retornos_diarios.index.year, retornos_diarios.index.month]).apply(lambda x: (1 + x).prod() - 1)
        resampled.index.names = ['Año', 'Mes']
        df_matrix = resampled.unstack(level='Mes')
        
        # Mapear números de mes a abreviaturas estándar de tres letras
        meses_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        df_matrix = df_matrix.rename(columns=meses_dict)
        return df_matrix