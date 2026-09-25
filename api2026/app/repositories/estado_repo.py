from app.core.database import Database
from app.models.estado import Estado

class EstadoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM estado
            ORDER BY id_estado ASC;
        """)

        estados = cursor.fetchall()
        conn.close()

        return estados

    def obtener_por_id(self, estado_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM estado
            WHERE id_estado = %s;
        """, (estado_id,))

        estado = cursor.fetchone()
        conn.close()

        return estado

    def crear(self, estado: Estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO estado
            (nombre, categoria, descripcion)
            VALUES (%s, %s, %s)
            RETURNING id_estado;
        """

        cursor.execute(
            query,
            (
                estado.nombre,
                estado.categoria,
                estado.descripcion
            )
        )

        nuevo_id = cursor.fetchone()["id_estado"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, estado_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM estado
            WHERE id_estado = %s
            RETURNING id_estado;
        """, (estado_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, estado_id: int, estado: Estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE estado
            SET nombre = %s,
                categoria = %s,
                descripcion = %s
            WHERE id_estado = %s
            RETURNING id_estado;
        """

        cursor.execute(
            query,
            (
                estado.nombre,
                estado.categoria,
                estado.descripcion,
                estado_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None