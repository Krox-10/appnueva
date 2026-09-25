from app.core.database import Database
from app.models.recurso_semillero import RecursoSemillero

class RecursoSemilleroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM recurso_semillero
            ORDER BY id_recurso ASC;
        """)

        recursos = cursor.fetchall()
        conn.close()

        return recursos

    def obtener_por_id(self, recurso_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM recurso_semillero
            WHERE id_recurso = %s;
        """, (recurso_id,))

        recurso = cursor.fetchone()
        conn.close()

        return recurso

    def crear(self, recurso: RecursoSemillero):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO recurso_semillero
            (
                id_semillero,
                nombre,
                tipo,
                cantidad,
                descripcion,
                id_estado,
                fecha_registro
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_recurso;
        """

        cursor.execute(
            query,
            (
                recurso.id_semillero,
                recurso.nombre,
                recurso.tipo,
                recurso.cantidad,
                recurso.descripcion,
                recurso.id_estado,
                recurso.fecha_registro
            )
        )

        nuevo_id = cursor.fetchone()["id_recurso"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, recurso_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM recurso_semillero
            WHERE id_recurso = %s
            RETURNING id_recurso;
        """, (recurso_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, recurso_id: int, recurso: RecursoSemillero):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE recurso_semillero
            SET id_semillero = %s,
                nombre = %s,
                tipo = %s,
                cantidad = %s,
                descripcion = %s,
                id_estado = %s,
                fecha_registro = %s
            WHERE id_recurso = %s
            RETURNING id_recurso;
        """

        cursor.execute(
            query,
            (
                recurso.id_semillero,
                recurso.nombre,
                recurso.tipo,
                recurso.cantidad,
                recurso.descripcion,
                recurso.id_estado,
                recurso.fecha_registro,
                recurso_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None