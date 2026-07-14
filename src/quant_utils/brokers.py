from abc import ABC, abstractmethod
import pandas as pd

# =====================================================================
# INTFAZ BASE (ESTRATEGIA)
# =====================================================================
class BrokerStrategy(ABC):
    """Interfaz abstracta que define las reglas impositivas de cualquier Broker."""
    
    @abstractmethod
    def calcular_friccion(self, volumen_nominal: float) -> dict:
        pass


# =====================================================================
# ESTRATEGIAS CONCRETAS: INVIU 
# =====================================================================
class InviuSinAsesor(BrokerStrategy):
    def calcular_friccion(self, volumen_nominal: float) -> dict:
        # Según imagen_2.png: Hasta 2,00% por monto operado
        arancel_neto = volumen_nominal * 0.02
        iva = arancel_neto * 0.21
        return {
            "aranceles_netos": arancel_neto,
            "iva_sobre_comisiones": iva,
            "friccion_total": arancel_neto + iva,
            "detalle_broker": "Inviu SA (Sin Asesor - Arancel: 2.0% + IVA)"
        }

class InviuConAsesor(BrokerStrategy):
    def calcular_friccion(self, volumen_nominal: float) -> dict:
        # Según imagen_2.png: Hasta 1,50% por monto operado
        arancel_neto = volumen_nominal * 0.015
        iva = arancel_neto * 0.21
        return {
            "aranceles_netos": arancel_neto,
            "iva_sobre_comisiones": iva,
            "friccion_total": arancel_neto + iva,
            "detalle_broker": "Inviu SA (Con Asesor - Arancel: 1.5% + IVA)"
        }


# =====================================================================
# EL MOTOR DEL BROKER (CONTEXTO) Y LA FÁBRICA
# =====================================================================
class BrokerEngine:
    def __init__(self, broker_strategy: BrokerStrategy):
        self.broker = broker_strategy

    def simular_costos_operativos(self, df_pesos: pd.DataFrame, capital_inicial: float = 10000.0) -> dict:
        """Calcula el turnover e inyecta la fricción según el Broker elegido."""
        # Cambios absolutos en las ponderaciones entre periodos (t vs t-1)
        cambios_pesos = df_pesos.diff().abs().sum(axis=1)
        cambios_pesos.iloc[0] = df_pesos.iloc[0].abs().sum() # Primer rebalanceo
        
        turnover_acumulado = cambios_pesos.sum()
        volumen_bruto_nominal = turnover_acumulado * capital_inicial
        
        # Delegamos el cálculo a la estrategia del broker inyectado
        costos_broker = self.broker.calcular_friccion(volumen_bruto_nominal)
        
        return {
            "volumen_nominal_operado": volumen_bruto_nominal,
            "veces_rotado_capital": turnover_acumulado,
            "aranceles_netos": costos_broker["aranceles_netos"],
            "iva_sobre_comisiones": costos_broker["iva_sobre_comisiones"],
            "friccion_total_acumulada": costos_broker["friccion_total"],
            "label_broker": costos_broker["detalle_broker"]
        }

class BrokerFactory:
    """Fábrica estática para instanciar brokers de forma limpia mediante strings."""
    _brokers = {
        "inviu_sin_asesor": InviuSinAsesor,
        "inviu_con_asesor": InviuConAsesor
    }
    
    @classmethod
    def obtener_broker(cls, nombre_broker: str) -> BrokerEngine:
        broker_class = cls._brokers.get(nombre_broker.lower())
        if not broker_class:
            raise ValueError(f"El broker '{nombre_broker}' no está registrado en el sistema.")
        return BrokerEngine(broker_class())