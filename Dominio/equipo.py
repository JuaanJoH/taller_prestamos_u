from dataclasses import dataclass
from Dominio.categoria import Categoria

@dataclass
class Equipo:
    id: int
    nombre: str
    categoria: Categoria
    estado: str

    
    def get_estado(self) -> str:
        return self.estado

    def get_nombre(self) -> str:
        return self.nombre
    
    def set_estado(self, estado: str) -> None:
        self.estado = estado

    def set_nombre(self, nombre: str) -> None:
        self.nombre = nombre