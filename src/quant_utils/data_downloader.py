# src/quants_utils/data_downloader.py

import yfinance as yf
import pandas as pd
from pathlib import Path

class DataDownloader:
    # Detecta la raíz del proyecto (sube 2 niveles desde quants_utils/)
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    @classmethod
    def download_portfolio_data(cls, tickers: list, start_date: str, end_date: str, filename: str = "precios.parquet") -> pd.DataFrame:
        """
        Descarga datos de Yahoo Finance y los almacena en data/raw de manera limpia.
        """
        print(f"- Iniciando descarga de: {tickers}")
        print(f"- Período: {start_date} al {end_date}")
        
        # Descarga usando Adjusted Close para contemplar dividendos y splits
        data = yf.download(tickers, start=start_date, end=end_date)
        
        if 'Adj Close' in data.columns:
            df = data['Adj Close']
        else:
            df = data['Close']
            
        # Si elegís un solo activo, Yahoo devuelve una Serie. La pasamos a DataFrame.
        if isinstance(df, pd.Series):
            df = df.to_frame(name=tickers[0])
            
        # Asegurar que el índice esté limpio y sin zonas horarias molestas
        df = df.copy()                     # Evita el SettingWithCopyWarning
        df = df.astype(float)             # Fuerza a que todo sea float puro, eliminando objetos de Python
        df.index = pd.to_datetime(df.index).date # Limpia el índice temporal
        df.index.name = 'Fecha'
        
        # Guardar en la carpeta correcta usando la estructura estándar
        raw_path = cls.BASE_DIR / "data" / "raw"
        raw_path.mkdir(parents=True, exist_ok=True)
        
        output_path = raw_path / filename
        df.to_parquet(output_path)
        
        print(f"¡Datos guardados exitosamente en: {output_path}!")
        print(f"Registros: {df.shape[0]} días de mercado | {df.shape[1]} activos.")
        return df

if __name__ == "__main__":
    # Test rápido de ejecución si corres el archivo directamente
    activos_default = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"]
    DataDownloader.download_portfolio_data(
        tickers=activos_default, 
        start_date="2024-01-01", 
        end_date="2025-12-31"
    )