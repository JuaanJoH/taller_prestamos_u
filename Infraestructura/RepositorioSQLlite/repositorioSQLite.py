import sqlite3
from datetime import date

from Aplicacion.Puertos.repositorioEstudiante import RepositorioEstudiante
from Aplicacion.Puertos.repositorioEquipo import RepositorioEquipo
from Aplicacion.Puertos.repositorioPrestamo import RepositorioPrestamo
from Dominio.estudiante import Estudiante
from Dominio.equipo import Equipo
from Dominio.prestamo import Prestamo
from Dominio.portatil import Portatil
from Dominio.camara import Camara
from Dominio.kitRobotica import KitRobotica

CATEGORIAS_EQUIPOS = {
    "PORTATIL":     Portatil(),
    "CAMARA":       Camara(),
    "KIT_ROBOTICA": KitRobotica(),
}


class RepositorioSQLite(RepositorioEstudiante, RepositorioEquipo, RepositorioPrestamo):

    def __init__(self, ruta_db: str):
        self.db = sqlite3.connect(ruta_db)
        self._crear_tablas()

    def _crear_tablas(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                cedula            TEXT PRIMARY KEY,
                nombre            TEXT,
                correo            TEXT,
                multas_pendientes INTEGER,
                prestamos_activos INTEGER
            )""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS equipos (
                id        TEXT PRIMARY KEY,
                nombre    TEXT,
                categoria TEXT,
                estado    TEXT
            )""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id                TEXT PRIMARY KEY,
                cedula_estudiante TEXT,
                id_equipo         TEXT,
                fecha_prestamo    TEXT,
                fecha_limite      TEXT,
                fecha_devolucion  TEXT,
                multa_a_cobrar    INTEGER
            )""")
        self.db.commit()


    # Estudiante 


    def guardarEstudiante(self, estudiante: Estudiante) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO estudiantes VALUES (?,?,?,?,?)",
            (estudiante.cedula, estudiante.nombre, estudiante.correo,
             estudiante.multas_pendientes, estudiante.prestamos_activos)
        )
        self.db.commit()

    def buscarEstudiante(self, cedula: str) -> Estudiante:
        fila = self.db.execute(
            "SELECT * FROM estudiantes WHERE cedula=?", (cedula,)
        ).fetchone()
        return Estudiante(
            cedula = fila[0],
            nombre = fila[1],
            correo = fila[2],
            multas_pendientes = fila[3],
            prestamos_activos = fila[4]
        )


    # Equipo 


    def guardarEquipo(self, equipo: Equipo) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO equipos VALUES (?,?,?,?)",
            (equipo.id, equipo.nombre, equipo.categoria.nombre, equipo.estado)
        )
        self.db.commit()

    def buscarEquipo(self, id_equipo: str) -> Equipo:
        fila = self.db.execute(
            "SELECT * FROM equipos WHERE id=?", (id_equipo,)
        ).fetchone()
        return Equipo(
            id = fila[0],
            nombre = fila[1],
            categoria = CATEGORIAS_EQUIPOS[fila[2]],
            estado = fila[3]
        )


    # Prestamo 

    def guardarPrestamo(self, prestamo: Prestamo) -> None:
        fecha_dev = prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
        self.db.execute(
            "INSERT OR REPLACE INTO prestamos VALUES (?,?,?,?,?,?,?)",
            (prestamo.id,
             prestamo.estudiante.cedula,
             prestamo.equipo.id,
             prestamo.fecha_prestamo.isoformat(),
             prestamo.fecha_limite.isoformat(),
             fecha_dev,
             prestamo.multa_a_cobrar)
        )
        self.db.commit()

    def buscarPrestamo(self, id_prestamo: str) -> Prestamo:
        fila = self.db.execute(
            "SELECT * FROM prestamos WHERE id=?", (id_prestamo,)
        ).fetchone()
        return self._fila_a_prestamo(fila)

    def buscarPrestamoActivoPorEquipo(self, id_equipo: str) -> Prestamo:
        fila = self.db.execute(
            "SELECT * FROM prestamos WHERE id_equipo=? AND fecha_devolucion IS NULL",
            (id_equipo,)
        ).fetchone()
        return self._fila_a_prestamo(fila)


    # Privado


    def _fila_a_prestamo(self, fila) -> Prestamo:
        estudiante = self.buscarEstudiante(fila[1])
        equipo     = self.buscarEquipo(fila[2])
        fecha_dev  = date.fromisoformat(fila[5]) if fila[5] else None
        return Prestamo(
            id = fila[0],
            estudiante = estudiante,
            equipo = equipo,
            fecha_prestamo = date.fromisoformat(fila[3]),
            fecha_limite = date.fromisoformat(fila[4]),
            fecha_devolucion = fecha_dev,
            multa_a_cobrar = fila[6]
        )
