from dataclasses import dataclass
from datetime import date
from Dominio.estudiante import Estudiante
from Dominio.equipo import Equipo

@dataclass
class Prestamo:
    id: int
    estudiante: Estudiante
    equipo: Equipo
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date
    multa_cobrada: int

    def confirmar(self) -> bool:
        pass

    def negar(self) -> bool:
        pass

    def calcular_multa(self) -> int:
        pass

