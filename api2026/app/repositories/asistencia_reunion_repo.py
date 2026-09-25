from app.core.database import Database
from app.models.asistencia_reunion import AsistenciaReunion

class AsistenciaReunionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asistencia_reunion
            ORDER BY id_asistencia ASC;
        """)

        asistencias = cursor.fetchall()
        conn.close()

        return asistencias

    def obtener_por_id(self, asistencia_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asistencia_reunion
            WHERE id_asistencia = %s;
        """, (asistencia_id,))

        asistencia = cursor.fetchone()
        conn.close()

        return asistencia

    def crear(self, asistencia: AsistenciaReunion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO asistencia_reunion
            (
                id_reunion,
                id_usuario,
                asistio,
                observacion
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_asistencia;
        """

        cursor.execute(
            query,
            (
                asistencia.id_reunion,
                asistencia.id_usuario,
                asistencia.asistio,
                asistencia.observacion
            )
        )

        nuevo_id = cursor.fetchone()["id_asistencia"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, asistencia_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM asistencia_reunion
            WHERE id_asistencia = %s
            RETURNING id_asistencia;
        """, (asistencia_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(
        self,
        asistencia_id: int,
        asistencia: AsistenciaReunion
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE asistencia_reunion
            SET id_reunion = %s,
                id_usuario = %s,
                asistio = %s,
                observacion = %s
            WHERE id_asistencia = %s
            RETURNING id_asistencia;
        """

        cursor.execute(
            query,
            (
                asistencia.id_reunion,
                asistencia.id_usuario,
                asistencia.asistio,
                asistencia.observacion,
                asistencia_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None