from dataclasses import dataclass
from abc import ABC

@dataclass
class Categoria(ABC):
    nombre: str
    plazo_prestamo_dias: int
    tarifa_multa: int


    def get_nombre(self) -> str:
        return self.nombre

    def get_plazo_prestamo_dias(self) -> int:
        return self.plazo_prestamo_dias

    def get_tarifa_multa(self) -> int:
        return self.tarifa_multa