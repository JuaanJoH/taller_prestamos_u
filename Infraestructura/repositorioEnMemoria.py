from Aplicacion.Puertos.repositorioEstudiante import RepositorioEstudiante
from Aplicacion.Puertos.repositorioEquipo import RepositorioEquipo
from Aplicacion.Puertos.repositorioPrestamo import RepositorioPrestamo
from Dominio.estudiante import Estudiante
from Dominio.equipo import Equipo
from Dominio.prestamo import Prestamo


class RepositorioEnMemoria(RepositorioEstudiante, RepositorioEquipo, RepositorioPrestamo):

    def __init__(self):
        self._estudiantes: list[Estudiante] = []
        self._equipos:     list[Equipo]     = []
        self._prestamos:   list[Prestamo]   = []


    # Estudiante

    def guardarEstudiante(self, estudiante: Estudiante) -> None:
        for i, e in enumerate(self._estudiantes):
            if e.cedula == estudiante.cedula:
                self._estudiantes[i] = estudiante
                return
        self._estudiantes.append(estudiante)

    def buscarEstudiante(self, cedula: str) -> Estudiante:
        for e in self._estudiantes:
            if e.cedula == cedula:
                return e
        raise ValueError(f"Estudiante '{cedula}' no encontrado")


    # Equipo

    def guardarEquipo(self, equipo: Equipo) -> None:
        for i, eq in enumerate(self._equipos):
            if eq.id == equipo.id:
                self._equipos[i] = equipo
                return
        self._equipos.append(equipo)

    def buscarEquipo(self, id_equipo: str) -> Equipo:
        for eq in self._equipos:
            if eq.id == id_equipo:
                return eq
        raise ValueError(f"Equipo '{id_equipo}' no encontrado")


    # Prestamo 

    def guardarPrestamo(self, prestamo: Prestamo) -> None:
        for i, p in enumerate(self._prestamos):
            if p.id == prestamo.id:
                self._prestamos[i] = prestamo
                return
        self._prestamos.append(prestamo)

    def buscarPrestamo(self, id_prestamo: str) -> Prestamo:
        for p in self._prestamos:
            if p.id == id_prestamo:
                return p
        raise ValueError(f"Préstamo '{id_prestamo}' no encontrado")

    def buscarPrestamoActivoPorEquipo(self, id_equipo: str) -> Prestamo:
        for p in self._prestamos:
            if p.equipo.id == id_equipo and p.fecha_devolucion is None:
                return p
        raise ValueError(f"No hay préstamo activo para el equipo '{id_equipo}'")
