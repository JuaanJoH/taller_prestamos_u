from datetime import timedelta
from uuid import uuid4
from Aplicacion.Puertos.repositorioPrestamo import RepositorioPrestamo
from Aplicacion.Puertos.repositorioEquipo import RepositorioEquipo
from Aplicacion.Puertos.repositorioEstudiante import RepositorioEstudiante
from Aplicacion.Puertos.notificaciones import Notificaciones
from Aplicacion.Puertos.proveedorFecha import ProveedorFecha
from Dominio.prestamo import Prestamo

class RegistrarPrestamo:
    def __init__(self, 
                repo_prestamo: RepositorioPrestamo, 
                repo_equipo: RepositorioEquipo, 
                repo_estudiante: RepositorioEstudiante, 
                notificaciones: Notificaciones, 
                proveedor_fecha: ProveedorFecha) -> None:

        self.repo_prestamo   = repo_prestamo
        self.repo_equipo     = repo_equipo
        self.repo_estudiante = repo_estudiante
        self.notificaciones  = notificaciones
        self.proveedor_fecha = proveedor_fecha

    def prestarEquipoAEstudiante(self, cedula: str, id_equipo: str) -> Prestamo:
        estudiante   = self.repo_estudiante.buscarEstudiante(cedula)
        equipo       = self.repo_equipo.buscarEquipo(id_equipo)
        fecha        = self.proveedor_fecha.hoy()
        fecha_limite = fecha + timedelta(days=equipo.categoria.plazo_prestamo_dias)

        prestamo = Prestamo(
            id             = str(uuid4())[:8],
            estudiante     = estudiante,
            equipo         = equipo,
            fecha_prestamo = fecha,
            fecha_limite   = fecha_limite,
        )

        prestamo.confirmar_prestamo()
        self.repo_estudiante.guardarEstudiante(prestamo.estudiante)  # persiste prestamos_activos
        self.repo_equipo.guardarEquipo(prestamo.equipo)              # persiste estado PRESTADO
        self.repo_prestamo.guardarPrestamo(prestamo)
        self.notificaciones.notificarPrestamo(prestamo)
        return prestamo