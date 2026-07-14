# src/quant-utils/optimization.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .stats import FinancialStats

class PortfolioOptimizer:
    """Clase encargada de ejecutar algoritmos de optimización de portafolios."""

    @staticmethod 
    def get_max_sharpe(retornos: pd.DataFrame, 
                       pesos_previos: np.ndarray = None, 
                       tasa_libre_riesgo: float = 0.0,
                       max_peso: float = 1.0,
                       gamma: float = 0.0) -> np.ndarray:
        """
        Encuentra los pesos que maximizan el Ratio de Sharpe.

        Optimización robusta:
        - Si pesos_previos es None, asume pesos iguales iniciales.
        - gamma: Factor de penalización por turnover (0 = sin penalización).
        """
        num_activos = retornos.shape[1]
        
        # 1. Normalización de inputs
        if pesos_previos is None:
            pesos_previos = np.ones(num_activos) / num_activos

        retornos_simples = np.exp(retornos) - 1
        media_anual = retornos_simples.mean() * 252
        cov_anual = retornos_simples.cov() * 252

        def objective(pesos):
            retorno_portafolio = np.sum(media_anual * pesos)
            volatilidad_portafolio = np.sqrt(np.dot(pesos.T, np.dot(cov_anual, pesos)))
            
            if volatilidad_portafolio == 0:
                return 0.0
                
            # Sharpe Ratio tradicional
            sharpe = (retorno_portafolio - tasa_libre_riesgo) / volatilidad_portafolio
            
            # Penalización por Turnover (Costo de transacción estimado/Fricción)
            # Al buscar minimizar la función, sumamos el costo para penalizar el desvío
            turnover = np.sum(np.abs(pesos - pesos_previos))
            
            return -sharpe + (gamma * turnover)
        # 3. Restricciones y límites (fijos y robustos)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = [(0, max_peso) for _ in range(num_activos)]
        
        try:
            res = minimize(
                fun=objective, 
                x0=pesos_previos, 
                bounds=bounds, 
                constraints=constraints,
                method='SLSQP',
                options={'ftol': 1e-7, 'maxiter': 200}
            )
            
            if res.success:
                return res.x
            else:
                # Si falla SLSQP, devolvemos un fallback limpio (1/N) o el previo mitigado
                return pesos_previos
                
        except Exception:
            return pesos_previos


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