from dataclasses import dataclass

@dataclass
class Categoria:
    nombre: str
    plazo_prestamo_dias: int
    tarifa_multa: int


    def get_nombre(self) -> str:
        return self.nombre

    def get_plazo_prestamo_dias(self) -> int:
        return self.plazo_prestamo_dias

    def get_tarifa_multa(self) -> int:
        return self.tarifa_multa