from app.core.database import Database
from app.models.investigacion_miembro import InvestigacionMiembro

class InvestigacionMiembroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM investigacion_miembro
            ORDER BY id_investigacion_miembro ASC;
        """)

        miembros = cursor.fetchall()
        conn.close()

        return miembros

    def obtener_por_id(self, miembro_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM investigacion_miembro
            WHERE id_investigacion_miembro = %s;
        """, (miembro_id,))

        miembro = cursor.fetchone()
        conn.close()

        return miembro

    def crear(self, miembro: InvestigacionMiembro):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO investigacion_miembro
            (
                id_investigacion,
                id_usuario,
                rol_investigacion,
                fecha_vinculacion
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_investigacion_miembro;
        """

        cursor.execute(
            query,
            (
                miembro.id_investigacion,
                miembro.id_usuario,
                miembro.rol_investigacion,
                miembro.fecha_vinculacion
            )
        )

        nuevo_id = cursor.fetchone()["id_investigacion_miembro"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, miembro_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM investigacion_miembro
            WHERE id_investigacion_miembro = %s
            RETURNING id_investigacion_miembro;
        """, (miembro_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(
        self,
        miembro_id: int,
        miembro: InvestigacionMiembro
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE investigacion_miembro
            SET id_investigacion = %s,
                id_usuario = %s,
                rol_investigacion = %s,
                fecha_vinculacion = %s
            WHERE id_investigacion_miembro = %s
            RETURNING id_investigacion_miembro;
        """

        cursor.execute(
            query,
            (
                miembro.id_investigacion,
                miembro.id_usuario,
                miembro.rol_investigacion,
                miembro.fecha_vinculacion,
                miembro_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None