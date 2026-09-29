from Dominio import Categoria
from dataclasses import dataclass

@dataclass
class kitRobotica(Categoria):
    nombre: str = "KIT_ROBOTICA"
    plazo_prestamo_dias: int = 1
    tarifa_multa: int = 12000
