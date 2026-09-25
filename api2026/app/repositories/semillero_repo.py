from app.core.database import Database
from app.models.semillero import Semillero

class SemilleroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM semillero
            ORDER BY id_semillero ASC;
        """)

        semilleros = cursor.fetchall()
        conn.close()

        return semilleros

    def obtener_por_id(self, semillero_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM semillero
            WHERE id_semillero = %s;
        """, (semillero_id,))

        semillero = cursor.fetchone()
        conn.close()

        return semillero

    def crear(self, semillero: Semillero):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO semillero
            (id_linea, nombre, descripcion, fecha_creacion, id_estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_semillero;
        """

        cursor.execute(
            query,
            (
                semillero.id_linea,
                semillero.nombre,
                semillero.descripcion,
                semillero.fecha_creacion,
                semillero.id_estado
            )
        )

        nuevo_id = cursor.fetchone()["id_semillero"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, semillero_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM semillero
            WHERE id_semillero = %s
            RETURNING id_semillero;
        """, (semillero_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, semillero_id: int, semillero: Semillero):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE semillero
            SET id_linea = %s,
                nombre = %s,
                descripcion = %s,
                fecha_creacion = %s,
                id_estado = %s
            WHERE id_semillero = %s
            RETURNING id_semillero;
        """

        cursor.execute(
            query,
            (
                semillero.id_linea,
                semillero.nombre,
                semillero.descripcion,
                semillero.fecha_creacion,
                semillero.id_estado,
                semillero_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None