from app.core.database import Database
from app.models.reunion import Reunion

class ReunionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM reunion
            ORDER BY id_reunion ASC;
        """)

        reuniones = cursor.fetchall()
        conn.close()

        return reuniones

    def obtener_por_id(self, reunion_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM reunion
            WHERE id_reunion = %s;
        """, (reunion_id,))

        reunion = cursor.fetchone()
        conn.close()

        return reunion

    def crear(self, reunion: Reunion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO reunion
            (
                id_semillero,
                fecha,
                hora_inicio,
                hora_fin,
                tema,
                descripcion,
                id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_reunion;
        """

        cursor.execute(
            query,
            (
                reunion.id_semillero,
                reunion.fecha,
                reunion.hora_inicio,
                reunion.hora_fin,
                reunion.tema,
                reunion.descripcion,
                reunion.id_estado
            )
        )

        nuevo_id = cursor.fetchone()["id_reunion"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, reunion_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM reunion
            WHERE id_reunion = %s
            RETURNING id_reunion;
        """, (reunion_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, reunion_id: int, reunion: Reunion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE reunion
            SET id_semillero = %s,
                fecha = %s,
                hora_inicio = %s,
                hora_fin = %s,
                tema = %s,
                descripcion = %s,
                id_estado = %s
            WHERE id_reunion = %s
            RETURNING id_reunion;
        """

        cursor.execute(
            query,
            (
                reunion.id_semillero,
                reunion.fecha,
                reunion.hora_inicio,
                reunion.hora_fin,
                reunion.tema,
                reunion.descripcion,
                reunion.id_estado,
                reunion_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None