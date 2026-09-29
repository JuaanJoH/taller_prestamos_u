from Dominio import Categoria
from dataclasses import dataclass

@dataclass
class Portatil(Categoria):
    nombre: str = "PORTATIL"
    plazo_prestamo_dias: int = 3
    tarifa_multa: int = 5000

