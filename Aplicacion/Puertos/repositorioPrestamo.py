from abc import ABC, abstractmethod
from Dominio.prestamo import Prestamo


class RepositorioPrestamo(ABC):

    @abstractmethod
    def guardarPrestamo(self, prestamo: Prestamo) -> None: ...

    @abstractmethod
    def buscarPrestamo(self, id_prestamo: str) -> Prestamo: ...

    @abstractmethod
    def buscarPrestamoActivoPorEquipo(self, id_equipo: str) -> Prestamo: ...
