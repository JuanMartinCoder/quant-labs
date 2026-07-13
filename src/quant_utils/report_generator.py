from .stats import FinancialStats
from .plotting import QuantPlotter
import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors


class ReportGenerator:

    def __init__(self, output_path):
        self.doc = SimpleDocTemplate(output_path, pagesize=A4)
        self.styles = getSampleStyleSheet()

    def create_table(self, data, header_color=colors.navy):
        """Crea tablas con el estilo institucional oscuro que mostraste."""
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), header_color),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ])
        table.setStyle(style)
        return table
    @staticmethod
    def generar_reporte_completo(data_equity: pd.Series, metricas: dict, ruta_salida: str):
        """
        Ensambla el reporte completo:
        1. Curva de Rendimiento (Equity Curve)
        2. Tabla de KPIs (Sharpe, Sortino, MDD)
        3. Gráfico de rotación (Turnover)
        4. Distribución de pesos finales
        """
        # Aquí llamarías a tu lógica de visualización (QuantPlotter)
        # y guardarías el resultado final como PDF o imagen consolidada.
        pass