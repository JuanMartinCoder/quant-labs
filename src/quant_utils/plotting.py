# src/quant_utils/plotting.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .stats import FinancialStats
from .optimization import PortfolioOptimizer

# Configuración estética global
sns.set_theme(style="darkgrid")

class QuantPlotter:
    """Clase encargada de generar visualizaciones financieras avanzadas."""

    @staticmethod
    def graficar_frontera_eficiente(retornos: pd.DataFrame, 
                                    periodos_ano: int = 252) -> None:
        """
        Genera una simulación de Monte Carlo y grafica la Frontera Eficiente,
        resaltando los portafolios óptimos.
        """
        num_activos = len(retornos.columns)
        num_portafolios = 5000
        
        resultados_ret = []
        resultados_vol = []
        resultados_sharpe = []
        
        # Simulación Monte Carlo
        for _ in range(num_portafolios):
            pesos = np.random.random(num_activos)
            pesos /= np.sum(pesos)
            
            ret_p, vol_p = FinancialStats.metricas_portafolio(pesos, retornos, periodos_ano)
            resultados_ret.append(ret_p)
            resultados_vol.append(vol_p)
            resultados_sharpe.append(ret_p / vol_p if vol_p != 0 else 0)
            
        # Puntos óptimos reales
        pesos_sh = PortfolioOptimizer.max_sharpe(retornos, periodos_ano=periodos_ano)
        ret_sh, vol_sh = FinancialStats.metricas_portafolio(pesos_sh, retornos, periodos_ano)
        
        pesos_vol = PortfolioOptimizer.minima_volatilidad(retornos, periodos_ano=periodos_ano)
        ret_vol, vol_vol = FinancialStats.metricas_portafolio(pesos_vol, retornos, periodos_ano)
        
        # Gráfico
        plt.figure(figsize=(11, 6))
        scatter = plt.scatter(resultados_vol, resultados_ret, c=resultados_sharpe, 
                              cmap='viridis', marker='o', s=10, alpha=0.3)
        plt.colorbar(scatter, label='Ratio de Sharpe')
        
        plt.scatter(vol_sh, ret_sh, color='red', marker='*', s=200, 
                    label=f'Máximo Sharpe ({ret_sh*100:.1f}% Ret, {vol_sh*100:.1f}% Vol)')
        plt.scatter(vol_vol, ret_vol, color='blue', marker='*', s=200, 
                    label=f'Mínima Volatilidad ({ret_vol*100:.1f}% Ret, {vol_vol*100:.1f}% Vol)')
        
        plt.title('Frontera Eficiente de Markowitz', fontsize=12, fontweight='bold')
        plt.xlabel('Volatilidad Anualizada (Riesgo)')
        plt.ylabel('Retorno Esperado Anualizado')
        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()