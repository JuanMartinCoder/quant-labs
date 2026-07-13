# src/quant-utils/optimization.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .stats import FinancialStats

class PortfolioOptimizer:
    """Clase encargada de ejecutar algoritmos de optimización de portafolios."""

    @staticmethod 
    def max_sharpe(retornos: pd.DataFrame, 
                   pesos_actuales: np.ndarray = None,
                   tasa_libre_riesgo: float = 0.0, 
                   periodos_ano: int = 252,
                   max_peso: float = 1.0,
                   factor_penalizacion: float = 0.1) -> np.ndarray:
        """
        Encuentra los pesos que maximizan el Ratio de Sharpe.
        """
        num_activos = len(retornos.columns)
        
        if pesos_actuales is None:
            pesos_actuales = np.zeros(len(retornos.columns))
        # Función objetivo: Minimizar el Sharpe negativo es equivalente a maximizar el Sharpe positivo
        def funcion_objetivo(pesos: np.ndarray) -> float:
            ret_p, vol_p = FinancialStats.metricas_portafolio(pesos, retornos, periodos_ano)
            sharpe = (ret_p - tasa_libre_riesgo) / vol_p

            if np.sum(pesos_actuales) == 0:
                costo_rotacion = 0.0
            else:
                costo_rotacion = np.sum(np.abs(pesos - pesos_actuales)) * factor_penalizacion

            return -sharpe + costo_rotacion

        # Restricciones de igualdad: sum(w) = 1  --> sum(w) - 1 = 0
        restricciones = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        
        # Límites: Pesos entre 0 y 1 por activo (No short-selling, no apalancamiento)
        limites = tuple((0.0, max_peso) for _ in range(num_activos))

        
        # Conjetura inicial: Distribución equitativa
        x0 = pesos_actuales if np.sum(pesos_actuales) > 0 else np.array([1.0 / num_activos] * num_activos)
        
        resultado = minimize(
            fun=funcion_objetivo,
            x0=x0,
            method='SLSQP',
            bounds=limites,
            constraints=restricciones
        )
        
        if not resultado.success:
            raise ValueError(f"La optimización falló: {resultado.message}")
            
        return resultado.x

    @staticmethod
    def minima_volatilidad(retornos: pd.DataFrame, periodos_ano: int = 252) -> np.ndarray:
        """
        Encuentra los pesos que minimizan el riesgo absoluto (volatilidad) del portafolio.
        """
        num_activos = len(retornos.columns)
        
        # Función objetivo: Minimizar la volatilidad directamente
        def funcion_objetivo(pesos: np.ndarray) -> float:
            _, vol_p = FinancialStats.metricas_portafolio(pesos, retornos, periodos_ano)
            return vol_p

        restricciones = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        limites = tuple((0.0, 1.0) for _ in range(num_activos))
        pesos_iniciales = np.array([1.0 / num_activos] * num_activos)
        
        resultado = minimize(
            fun=funcion_objetivo,
            x0=pesos_iniciales,
            method='SLSQP',
            bounds=limites,
            constraints=restricciones
        )
        
        if not resultado.success:
            raise ValueError(f"La optimización falló: {resultado.message}")
            
        return resultado.x