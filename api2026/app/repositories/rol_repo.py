from app.core.database import Database
from app.models.rol import Rol

class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM rol
            ORDER BY id_rol ASC;
        """)

        roles = cursor.fetchall()
        conn.close()

        return roles

    def obtener_por_id(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM rol
            WHERE id_rol = %s;
        """, (rol_id,))

        rol = cursor.fetchone()
        conn.close()

        return rol

    def crear(self, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO rol
            (nombre, descripcion, id_estado)
            VALUES (%s, %s, %s)
            RETURNING id_rol;
        """

        cursor.execute(
            query,
            (
                rol.nombre,
                rol.descripcion,
                rol.id_estado
            )
        )

        nuevo_id = cursor.fetchone()["id_rol"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM rol
            WHERE id_rol = %s
            RETURNING id_rol;
        """, (rol_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, rol_id: int, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE rol
            SET nombre = %s,
                descripcion = %s,
                id_estado = %s
            WHERE id_rol = %s
            RETURNING id_rol;
        """

        cursor.execute(
            query,
            (
                rol.nombre,
                rol.descripcion,
                rol.id_estado,
                rol_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None