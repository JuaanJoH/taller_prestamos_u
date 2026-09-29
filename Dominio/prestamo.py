from dataclasses import dataclass
from datetime import date, timedelta
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
    multa_cobrada: int = 0

    def confirmar_prestamo(self) -> None:
        if self.estudiante is None or self.equipo is None:
            raise ValueError("El prestamo debe tener un estudiante y un equipo")
        self.estudiante.validar_multas_pendientes()
        self.estudiante.validar_prestamos_activos()
        self.equipo.prestar()
        self.estudiante.add_prestamos_activos()

    def confirmar_devolucion(self) -> None:
        self.equipo.devolver()
        self.estudiante.sub_prestamos_activos()

    def calcular_fecha_limite(self) -> date:
        self.fecha_limite = self.fecha_prestamo + timedelta(days=self.equipo.get_categoria().get_plazo_prestamo_dias())
        return self.fecha_limite
        
        