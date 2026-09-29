from Dominio import Categoria
from dataclasses import dataclass

@dataclass
class Camara(Categoria):
    nombre: str = "CAMARA"
    plazo_prestamo_dias: int = 2
    tarifa_multa: int = 8000

