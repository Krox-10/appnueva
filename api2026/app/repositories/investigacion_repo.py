from app.core.database import Database
from app.models.investigacion import Investigacion

class InvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM investigacion
            ORDER BY id_investigacion ASC;
        """)

        investigaciones = cursor.fetchall()
        conn.close()

        return investigaciones

    def obtener_por_id(self, investigacion_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM investigacion
            WHERE id_investigacion = %s;
        """, (investigacion_id,))

        investigacion = cursor.fetchone()
        conn.close()

        return investigacion

    def crear(self, investigacion: Investigacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO investigacion
            (
                id_semillero,
                titulo,
                descripcion,
                fecha_inicio,
                fecha_finalizacion,
                id_estado,
                archivo_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_investigacion;
        """

        cursor.execute(
            query,
            (
                investigacion.id_semillero,
                investigacion.titulo,
                investigacion.descripcion,
                investigacion.fecha_inicio,
                investigacion.fecha_finalizacion,
                investigacion.id_estado,
                investigacion.archivo_url
            )
        )

        nuevo_id = cursor.fetchone()["id_investigacion"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, investigacion_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM investigacion
            WHERE id_investigacion = %s
            RETURNING id_investigacion;
        """, (investigacion_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, investigacion_id: int, investigacion: Investigacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE investigacion
            SET id_semillero = %s,
                titulo = %s,
                descripcion = %s,
                fecha_inicio = %s,
                fecha_finalizacion = %s,
                id_estado = %s,
                archivo_url = %s
            WHERE id_investigacion = %s
            RETURNING id_investigacion;
        """

        cursor.execute(
            query,
            (
                investigacion.id_semillero,
                investigacion.titulo,
                investigacion.descripcion,
                investigacion.fecha_inicio,
                investigacion.fecha_finalizacion,
                investigacion.id_estado,
                investigacion.archivo_url,
                investigacion_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None