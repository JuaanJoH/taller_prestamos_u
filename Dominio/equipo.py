from dataclasses import dataclass
from Dominio.categoria import Categoria

@dataclass
class Equipo:
    id: int
    nombre: str
    categoria: Categoria
    estado: str

    # Getters

    def get_estado(self) -> str:
        return self.estado

    def get_nombre(self) -> str:
        return self.nombre

    def get_categoria(self) -> Categoria:
        return self.categoria

    # Setters
    
    def set_estado(self, estado: str) -> None:
        self.estado = estado

    def set_nombre(self, nombre: str) -> None:
        self.nombre = nombre

    def prestar(self) -> None:
        if self.estado != "DISPONIBLE":
            raise ValueError("No se puede prestar un equipo no disponible")
        self.estado = "PRESTADO"

    def devolver(self, hay_daños: bool) -> None:
        if hay_daños:
            self.estado = "EN_MANTENIMIENTO"
        self.estado = "DISPONIBLE"