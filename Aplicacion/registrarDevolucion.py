from Aplicacion.Puertos.repositorioPrestamo   import RepositorioPrestamo
from Aplicacion.Puertos.repositorioEquipo     import RepositorioEquipo
from Aplicacion.Puertos.repositorioEstudiante import RepositorioEstudiante
from Aplicacion.Puertos.notificaciones        import Notificaciones
from Aplicacion.Puertos.proveedorFecha import ProveedorFecha

class RegistrarDevolucion:
    def __init__(self,
                 repo_prestamo: RepositorioPrestamo,
                 repo_equipo: RepositorioEquipo,
                 repo_estudiante: RepositorioEstudiante,
                 notificacion: Notificaciones,
                 proveedor_fecha: ProveedorFecha):

        self.repo_prestamo = repo_prestamo
        self.repo_equipo = repo_equipo
        self.repo_estudiante = repo_estudiante
        self.notificacion = notificacion
        self.proveedor_fecha = proveedor_fecha

    def devolucionEquipoPorEstudiante(self, id_prestamo:str, hay_daños:bool) -> None:
        prestamo = self.repo_prestamo.buscarPrestamo(id_prestamo)
        fecha_devolucion = self.proveedor_fecha.hoy()
        prestamo.confirmar_devolucion(fecha_devolucion, hay_daños)

        if prestamo.multa_a_cobrar > 0:
            self.notificacion.notificarMulta(prestamo)

        self.repo_prestamo.guardarPrestamo(prestamo)
        self.repo_equipo.guardarEquipo(prestamo.equipo)
        self.repo_estudiante.guardarEstudiante(prestamo.estudiante)


        