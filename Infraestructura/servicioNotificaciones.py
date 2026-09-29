from Aplicacion.Puertos.notificaciones import Notificaciones
from Dominio.prestamo import Prestamo

class ServicioNotificaciones(Notificaciones):
    
    def notificarPrestamo(self, prestamo: Prestamo) -> None:
        print(f"[NOTIFICACIÓN] {prestamo.estudiante.nombre}: "
              f"préstamo de {prestamo.equipo.nombre} "
              f"hasta {prestamo.fecha_limite}")

            
    def notificarMulta(self, prestamo: Prestamo) -> None:
        print(f"[NOTIFICACIÓN] {prestamo.estudiante.nombre}: "
              f"multa de ${prestamo.multa_a_cobrar:,} generada.")