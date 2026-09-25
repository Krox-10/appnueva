from app.core.database import Database
from app.models.linea_investigacion import LineaInvestigacion

class LineaInvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM linea_investigacion
            ORDER BY id_linea ASC;
        """)

        lineas = cursor.fetchall()
        conn.close()

        return lineas

    def obtener_por_id(self, linea_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM linea_investigacion
            WHERE id_linea = %s;
        """, (linea_id,))

        linea = cursor.fetchone()
        conn.close()

        return linea

    def crear(self, linea: LineaInvestigacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO linea_investigacion
            (nombre, descripcion, fecha_creacion, id_estado)
            VALUES (%s, %s, %s, %s)
            RETURNING id_linea;
        """

        cursor.execute(
            query,
            (
                linea.nombre,
                linea.descripcion,
                linea.fecha_creacion,
                linea.id_estado
            )
        )

        nuevo_id = cursor.fetchone()["id_linea"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, linea_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM linea_investigacion
            WHERE id_linea = %s
            RETURNING id_linea;
        """, (linea_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, linea_id: int, linea: LineaInvestigacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE linea_investigacion
            SET nombre = %s,
                descripcion = %s,
                fecha_creacion = %s,
                id_estado = %s
            WHERE id_linea = %s
            RETURNING id_linea;
        """

        cursor.execute(
            query,
            (
                linea.nombre,
                linea.descripcion,
                linea.fecha_creacion,
                linea.id_estado,
                linea_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None