# src/quants_utils/reports/plotting.py

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from .styles import InstitutionalStyle

class QuantPlotter:
    BASE_DIR = Path(__file__).resolve().parents[3]
    TMP_DIR = BASE_DIR / "data" / "interim"

    @classmethod
    def _setup_style(cls):
        """Configura los parámetros estéticos globales de Matplotlib."""
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['figure.facecolor'] = '#ffffff'

    @classmethod
    def generar_graficos_reporte(cls, equity_curve: pd.DataFrame, pesos_actuales: pd.Series):
        """Genera y exporta la curva de patrimonio y el gráfico de asignación (torta)."""
        cls._setup_style()
        cls.TMP_DIR.mkdir(parents=True, exist_ok=True)
        
        # 1. Gráfico de Evolución del Capital (Evolución Diaria)
        fig, ax = plt.subplots(figsize=(7, 3.5), dpi=300)
        for col in equity_curve.columns:
            linewidth = 2.0 if "Dinámico" in col else 1.2
            alpha = 1.0 if "Dinámico" in col else 0.7
            ax.plot(equity_curve.index, equity_curve[col], label=col, linewidth=linewidth, alpha=alpha)
        
        ax.set_title("Evolución del Capital Diario ($)\nBacktesting Corporativo", fontsize=10, fontweight='bold', color=InstitutionalStyle.PRIMARY_BLUE)
        ax.set_ylabel("Valor de la Cartera (USD)", fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        ax.legend(fontsize=7, loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.5, color=InstitutionalStyle.GRID_COLOR)
        
        plot_path_line = cls.TMP_DIR / "equity_curve.png"
        plt.tight_layout()
        plt.savefig(plot_path_line, bbox_inches='tight', transparent=True)
        plt.close()

        # 2. Gráfico de Torta (Asset Allocation para el Próximo Período)
        fig, ax = plt.subplots(figsize=(5, 3.5), dpi=300)
        colores_torta = ['#1abc9c', '#3498db', '#9b59b6', '#f1c40f', '#e67e22', '#e74c3c']
        
        # Filtrar activos con peso mayor a 0 para que no encimen etiquetas
        pesos_filtrados = pesos_actuales[pesos_actuales > 0.01]
        
        ax.pie(
            pesos_filtrados, 
            labels=pesos_filtrados.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colores_torta[:len(pesos_filtrados)],
            textprops={'fontsize': 7, 'weight': 'bold'}
        )
        ax.set_title("Asignación de Pesos Actuales\npara Próximo Período", fontsize=10, fontweight='bold', color=InstitutionalStyle.PRIMARY_BLUE)
        
        plot_path_pie = cls.TMP_DIR / "asset_allocation.png"
        plt.tight_layout()
        plt.savefig(plot_path_pie, bbox_inches='tight', transparent=True)
        plt.close()
        
        return str(plot_path_line), str(plot_path_pie)