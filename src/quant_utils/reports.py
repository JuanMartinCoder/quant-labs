# src/quant_utils/reports.py

import os
import base64
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

class ReportGenerator:
    """Clase encargada de consolidar métricas y compilar reportes profesionales en PDF."""
    
    @staticmethod
    def _convertir_a_base64(file_path):
        """Función auxiliar para blindar rutas convirtiendo imágenes a Data URIs."""
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as img:
                encoded = base64.b64encode(img.read()).decode('utf-8')
                return f"data:image/png;base64,{encoded}"
        return None

    @staticmethod
    def generar_reporte_backtest(estrategias_data: list, costos_data: dict, broker_name: str, 
                                 grafico_path: str = None, grafico_pie_path: str = None, 
                                 output_filename: str = "reporte_backtest.pdf"):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, "templates")
        
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report_template.html")
        
        contexto = {
            "analista": "Juan Martin Rodriguez",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "broker_name": broker_name,
            "estrategias": estrategias_data,
            "costos_data": costos_data,
            "grafico_path": ReportGenerator._convertir_a_base64(grafico_path),
            "grafico_pie_path": ReportGenerator._convertir_a_base64(grafico_pie_path)
        }
        
        html_renderizado = template.render(contexto)
        
        print(f"Compilando reporte institucional en: {output_filename}...")
        HTML(string=html_renderizado).write_pdf(output_filename)
        print("¡Reporte corporativo generado con éxito!")

        # --- Eliminar archivos temporales generados ---
        for path in [grafico_path, grafico_pie_path]:
            if path and os.path.exists(path):
                os.remove(path)