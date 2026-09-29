from abc import ABC, abstractmethod
from Dominio.estudiante import Estudiante


class RepositorioEstudiante(ABC):

    @abstractmethod
    def guardarEstudiante(self, estudiante: Estudiante) -> None: ...

    @abstractmethod
    def buscarEstudiante(self, cedula: str) -> Estudiante: ...
