from abc import ABC, abstractmethod
from datetime import date

class ProveedorFecha(ABC):

    @abstractmethod
    def hoy(self) -> date: ...