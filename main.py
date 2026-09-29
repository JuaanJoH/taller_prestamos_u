import os
from datetime import date

# Infraestructura
from Infraestructura.RepositorioSQLlite.repositorioSQLite import RepositorioSQLite
from Infraestructura.repositorioEnMemoria import RepositorioEnMemoria
from Infraestructura.servicioNotificaciones import ServicioNotificaciones
from Infraestructura.proveedorFechaFija import ProveedorFechaFija

# Dominio
from Dominio.estudiante import Estudiante
from Dominio.equipo import Equipo
from Dominio.prestamo import Prestamo
from Dominio.portatil import Portatil
from Dominio.camara import Camara
from Dominio.kitRobotica import KitRobotica

# Aplicacion
from Aplicacion.registrarPrestamo import RegistrarPrestamo
from Aplicacion.registrarDevolucion import RegistrarDevolucion


FECHA_DEMO      = date(2026, 10, 5)
FECHA_TARDÍA    = date(2026, 10, 6) 
RUTA_DB         = "laboratorio.db"


def construir_casos_de_uso(repo, notificacion, fecha):
    registrar_prestamo = RegistrarPrestamo(
        repo_prestamo   = repo,
        repo_equipo     = repo,
        repo_estudiante = repo,
        notificaciones  = notificacion,
        proveedor_fecha = fecha,
    )
    registrar_devolucion = RegistrarDevolucion(
        repo_prestamo   = repo,
        repo_equipo     = repo,
        repo_estudiante = repo,
        notificacion    = notificacion,
        proveedor_fecha = fecha,
    )
    return registrar_prestamo, registrar_devolucion


def cargar_datos_iniciales(repo):
    """Carga el estado inicial de la base de datos para el demo."""

    # Estudiantes
    ana  = Estudiante(cedula="1001", nombre="Ana",  correo="ana@lab.edu",  multas_pendientes=0, prestamos_activos=0)
    luis = Estudiante(cedula="2001", nombre="Luis", correo="luis@lab.edu", multas_pendientes=1, prestamos_activos=0)
    carlos = Estudiante(cedula="3001", nombre="Carlos", correo="carlos@lab.edu", multas_pendientes=0, prestamos_activos=1)
    repo.guardarEstudiante(ana)
    repo.guardarEstudiante(luis)
    repo.guardarEstudiante(carlos)

    # Equipos
    repo.guardarEquipo(Equipo(id="PORTATIL-01",    nombre="Portátil 1",     categoria=Portatil(),    estado="DISPONIBLE"))
    repo.guardarEquipo(Equipo(id="PORTATIL-02",    nombre="Portátil 2",     categoria=Portatil(),    estado="DISPONIBLE"))
    repo.guardarEquipo(Equipo(id="CAMARA-01",      nombre="Cámara 1",       categoria=Camara(),      estado="DISPONIBLE"))
    repo.guardarEquipo(Equipo(id="CAMARA-02",      nombre="Cámara 2",       categoria=Camara(),      estado="PRESTADO"))
    repo.guardarEquipo(Equipo(id="CAMARA-03",      nombre="Cámara 3",       categoria=Camara(),      estado="DISPONIBLE"))
    repo.guardarEquipo(Equipo(id="KITROBOTICA-01", nombre="Kit Robótica 1", categoria=KitRobotica(), estado="PRESTADO"))

    # Prestamo pre-existente de Carlos: CAMARA-02 prestada el 2026-10-01, limite 2026-10-03 (para CA3)
    camara2  = repo.buscarEquipo("CAMARA-02")
    repo.guardarPrestamo(Prestamo(
        id             = "P-CA3",
        estudiante     = carlos,
        equipo         = camara2,
        fecha_prestamo = date(2026, 10, 1),
        fecha_limite   = date(2026, 10, 3),
    ))

    # Prestamo pre-existente de Carlos: KITROBOTICA-01 activa (para que en CA5 se pueda devolver)
    kit01 = repo.buscarEquipo("KITROBOTICA-01")
    repo.guardarPrestamo(Prestamo(
        id             = "P-CA5",
        estudiante     = carlos,
        equipo         = kit01,
        fecha_prestamo = date(2026, 10, 4),
        fecha_limite   = date(2026, 10, 5),
    ))


def separador(titulo):
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print('='*55)


# Casos de aceptacion

def ca1_prestamo_exitoso(registrar_prestamo):
    separador("CA1: Ana pide PORTATIL-01 (debe aprobarse)")
    try:
        registrar_prestamo.prestarEquipoAEstudiante("1001", "PORTATIL-01")
        print("  [OK] Préstamo registrado. Fecha límite: 2026-10-08")
    except Exception as e:
        print(f"  [ERROR] Error inesperado: {e}")


def ca2_rechazo_por_limite(repo, registrar_prestamo):
    separador("CA2: Ana pide un tercer equipo (debe rechazarse)")
    ana    = repo.buscarEstudiante("1001")
    portatil2 = repo.buscarEquipo("PORTATIL-02")
    ana.add_prestamos_activos()
    portatil2.prestar()
    repo.guardarEstudiante(ana)
    repo.guardarEquipo(portatil2)
    repo.guardarPrestamo(Prestamo(
        id             = "P-ANA-2",
        estudiante     = ana,
        equipo         = portatil2,
        fecha_prestamo = FECHA_DEMO,
        fecha_limite   = FECHA_DEMO,
    ))
    try:
        registrar_prestamo.prestarEquipoAEstudiante("1001", "CAMARA-01")
        print("  [ERROR] Debió rechazarse pero se aprobó")
    except ValueError as e:
        print(f"  [OK] Rechazado correctamente: {e}")


def ca3_devolucion_tardia_con_multa(registrar_devolucion_tardia):
    separador("CA3: CAMARA-02 devuelta el 2026-10-06 (multa $24.000)")
    try:
        registrar_devolucion_tardia.devolucionEquipoPorEstudiante("P-CA3", False)
        print("  [OK] Devolución registrada con multa.")
    except Exception as e:
        print(f"  [ERROR] Error inesperado: {e}")


def ca4_rechazo_por_multa(registrar_prestamo):
    separador("CA4: Luis pide equipo con multa pendiente (debe rechazarse)")
    try:
        registrar_prestamo.prestarEquipoAEstudiante("2001", "CAMARA-01")
        print("  [ERROR] Debió rechazarse pero se aprobó")
    except ValueError as e:
        print(f"  [OK] Rechazado correctamente: {e}")


def ca5_devolucion_con_dano(registrar_devolucion, registrar_prestamo):
    separador("CA5: Equipo devuelto con dano -> EN_MANTENIMIENTO")
    try:
        registrar_devolucion.devolucionEquipoPorEstudiante("P-CA5", True)
        print("  [OK] Equipo en EN_MANTENIMIENTO.")
        registrar_prestamo.prestarEquipoAEstudiante("2001", "KITROBOTICA-01")
        print("  [ERROR] Debió rechazarse pero se aprobó")
    except ValueError as e:
        print(f"  [OK] No se puede prestar: {e}")


def demo_sqlite():
    print("\n" + "[ MODO DEMO - Repositorio SQLite ]".center(55))

    if os.path.exists(RUTA_DB):
        os.remove(RUTA_DB)

    repo         = RepositorioSQLite(RUTA_DB)
    notificacion = ServicioNotificaciones()
    fecha_demo   = ProveedorFechaFija(FECHA_DEMO)
    fecha_tardia = ProveedorFechaFija(FECHA_TARDÍA)

    cargar_datos_iniciales(repo)

    registrar_prestamo,   registrar_devolucion   = construir_casos_de_uso(repo, notificacion, fecha_demo)
    _,                    registrar_dev_tardia    = construir_casos_de_uso(repo, notificacion, fecha_tardia)

    ca1_prestamo_exitoso(registrar_prestamo)
    ca2_rechazo_por_limite(repo, registrar_prestamo)
    ca3_devolucion_tardia_con_multa(registrar_dev_tardia)
    ca4_rechazo_por_multa(registrar_prestamo)
    ca5_devolucion_con_dano(registrar_devolucion, registrar_prestamo)



def demo_memoria():
    print("\n" + "[ MODO DEMO - Repositorio en Memoria (LSP) ]".center(55))

    # ← Una sola línea diferente respecto a demo_sqlite()
    repo         = RepositorioEnMemoria()
    notificacion = ServicioNotificaciones()
    fecha_demo   = ProveedorFechaFija(FECHA_DEMO)
    fecha_tardia = ProveedorFechaFija(FECHA_TARDÍA)

    cargar_datos_iniciales(repo)

    registrar_prestamo,  registrar_devolucion  = construir_casos_de_uso(repo, notificacion, fecha_demo)
    _,                   registrar_dev_tardia   = construir_casos_de_uso(repo, notificacion, fecha_tardia)

    ca1_prestamo_exitoso(registrar_prestamo)
    ca2_rechazo_por_limite(repo, registrar_prestamo)
    ca3_devolucion_tardia_con_multa(registrar_dev_tardia)
    ca4_rechazo_por_multa(registrar_prestamo)
    ca5_devolucion_con_dano(registrar_devolucion, registrar_prestamo)



if __name__ == "__main__":
    demo_sqlite()
    demo_memoria()
