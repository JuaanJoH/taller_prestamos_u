from abc import ABC, abstractmethod
from Dominio.equipo import Equipo


class RepositorioEquipo(ABC):

    @abstractmethod
    def guardarEquipo(self, equipo: Equipo) -> None: ...

    @abstractmethod
    def buscarEquipo(self, id_equipo: str) -> Equipo: ...