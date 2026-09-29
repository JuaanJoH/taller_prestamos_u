from dataclasses import dataclass

@dataclass
class Estudiante:
    cedula: str
    nombre: str
    correo: str
    multas_pendientes: int = 0

    # Getters

    def get_cedula(self) -> str:
        return self.cedula

    def get_nombre(self) -> str:
        return self.nombre
    
    def get_correo(self) -> str:
        return self.correo
    
    def get_multas_pendientes(self) -> int:
        return self.multas_pendientes

    # Setters

    def set_cedula(self, cedula: str) -> None:
        self.cedula = cedula

    def set_nombre(self, nombre: str) -> None:
        self.nombre = nombre

    def set_correo(self, correo: str) -> None:
        self.correo = correo

    def set_multas_pendientes(self, multas_pendientes: int) -> None:
        self.multas_pendientes = multas_pendientes

    # Manejo de multas

    def add_multas_pendientes(self) -> None:
        self.multas_pendientes += 1

    def sub_multas_pendientes(self) -> None:
        self.multas_pendientes -= 1

    
