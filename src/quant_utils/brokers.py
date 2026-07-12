# src/quant_utils/brokers.py

from abc import ABC, abstractmethod

class BaseBroker(ABC):
    """Clase base abstracta para modelar las comisiones de cualquier Broker."""
    
    @abstractmethod
    def calcular_costo_transaccion(self, valor_operado: float) -> float:
        """Devuelve el costo total en dólares/moneda local por una operación."""
        pass


class Inviu(BaseBroker):
    """Modelo para el broker argentino Inviu.
    Aplica para operaciones en Mercado Local (Acciones, Bonos, CEDEARs, ONs).
    """
    def __init__(self, con_asesor: bool = False, derechos_mercado: float = 0.0008, considerar_iva: bool = True):
        """
        Parameters:
        -----------
        con_asesor : bool
            Si es True usa 1.50%. Si es False (autogestionado) usa 2.00%.
        derechos_mercado : float
            Arancel promedio de BYMA + tasas regulatorias (default 0.08%).
        considerar_iva : bool
            Si es True, le aplica el 21% de IVA al fee neto del broker.
        """
        # Según tabla: Sin asesor es hasta 2.00%, Con asesor hasta 1.50%
        base_fee = 0.015 if con_asesor else 0.020
        
        if considerar_iva:
            self.broker_fee = base_fee * 1.21
        else:
            self.broker_fee = base_fee
            
        self.derechos_mercado = derechos_mercado

    def calcular_costo_transaccion(self, valor_operado: float) -> float:
        # Costo total = (Comisión Broker + Derechos de Mercado) * Monto Operado
        fee_total_porcentual = self.broker_fee + self.derechos_mercado
        return valor_operado * fee_total_porcentual


class BrokerPorcentualGenerico(BaseBroker):
    """Modelo para brokers que cobran un esquema de porcentaje neto + impuestos.
    Sirve para brokers locales (ej. PPI, Balanz) o fintechs (ej. Robinhood con fee cripto).
    """
    def __init__(self, porcentaje_comision: float = 0.002, porcentaje_impuesto: float = 0.0001):
        self.fee = porcentaje_comision
        self.tax = porcentaje_impuesto

    def calcular_costo_transaccion(self, valor_operado: float) -> float:
        comision = valor_operado * self.fee
        impuestos = valor_operado * self.tax
        return comision + impuestos