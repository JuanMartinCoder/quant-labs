import pandas as pd
from pathlib import Path

class DataManager:
    # Ubicación base (la carpeta raíz de tu proyecto)
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    @classmethod
    def get_data_path(cls, folder: str, filename: str) -> Path:
        return cls.BASE_DIR / "data" / folder / filename

    @classmethod
    def load_parquet(cls, folder: str, filename: str) -> pd.DataFrame:
        path = cls.get_data_path(folder, filename)
        return pd.read_parquet(path)

    @classmethod
    def save_parquet(cls, df: pd.DataFrame, folder: str, filename: str):
        path = cls.get_data_path(folder, filename)
        # Asegura que la carpeta exista
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)

    @classmethod
    def save_report_data(cls, kpis, friccion, retornos_mensuales, pesos_historial):
        """Guarda todos los inputs necesarios para el reporte en una pasada."""
        cls.save_parquet(kpis, "processed", "kpis.parquet")
        cls.save_parquet(friccion, "processed", "friccion.parquet")
        cls.save_parquet(retornos_mensuales, "processed", "retornos_mensuales.parquet")
        cls.save_parquet(pesos_historial, "processed", "pesos_historial.parquet")