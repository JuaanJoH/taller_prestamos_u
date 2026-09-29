from dataclasses import dataclass

@dataclass
class Estudiante:
    cedula: str
    nombre: str
    correo: str
    multas_pendientes: int = 0
    prestamos_activos: int = 0

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

    # Logica de multas y prestamos

    def add_multas_pendientes(self) -> None:
        self.multas_pendientes += 1

    def sub_multas_pendientes(self) -> None:
        self.multas_pendientes -= 1

    def add_prestamos_activos(self) -> None:
        self.prestamos_activos += 1

    def sub_prestamos_activos(self) -> None:
        self.prestamos_activos -= 1

    def validar_multas_pendientes(self) -> None:
        if self.multas_pendientes > 0:
            raise ValueError("El estudiante tiene multas pendientes")

    def validar_prestamos_activos(self) -> None:
        if self.prestamos_activos > 2:
            raise ValueError("El estudiante tiene prestamos activos")
