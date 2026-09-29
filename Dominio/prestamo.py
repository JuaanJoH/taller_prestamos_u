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
    multa_a_cobrar: int = 0

    def confirmar_prestamo(self) -> None:
        if self.estudiante is None or self.equipo is None:
            raise ValueError("El prestamo debe tener un estudiante y un equipo")
        self.estudiante.validar_multas_pendientes()
        self.estudiante.validar_prestamos_activos()
        self.equipo.prestar()
        self.estudiante.add_prestamos_activos()

    def confirmar_devolucion(self, fecha_devolucion: date, hay_daños: bool) -> None:
        self.fecha_devolucion = fecha_devolucion
        self.equipo.devolver(hay_daños)
        self.estudiante.sub_prestamos_activos()
        dias_retraso = (self.fecha_devolucion - self.fecha_limite).days
        if dias_retraso > 0:
            self.estudiante.add_multas_pendientes()
            self.multa_a_cobrar = dias_retraso * self.equipo.get_categoria().get_tarifa_multa()
    

        
        