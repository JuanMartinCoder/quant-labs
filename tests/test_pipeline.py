from quant_utils import ReportGenerator

def test_pdf():
    print("Generando reporte de prueba...")
    report = ReportGenerator("test_reporte.pdf")
    report.add_header("REPORTE DE PRUEBA OPERATIVA")
    
    # Datos sintéticos
    data = [["Estrategia 1", "23.25%", "0.85"], ["Estrategia 2", "22.87%", "0.76"]]
    report.add_table(data, ["Estrategia", "Retorno", "Sharpe"])
    
    report.generate()
    print("¡Listo! El archivo test_reporte.pdf debería estar en tu carpeta raíz.")

if __name__ == "__main__":
    test_pdf()