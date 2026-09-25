from app.core.database import Database
from app.models.usuario import Usuario

class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuario
            ORDER BY id_usuario ASC;
        """)

        usuarios = cursor.fetchall()
        conn.close()

        return usuarios

    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuario
            WHERE id_usuario = %s;
        """, (usuario_id,))

        usuario = cursor.fetchone()
        conn.close()

        return usuario

    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO usuario
            (
                id_rol,
                id_semillero,
                nombre_usuario,
                correo,
                documento,
                telefono,
                fecha_registro,
                id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_usuario;
        """

        cursor.execute(
            query,
            (
                usuario.id_rol,
                usuario.id_semillero,
                usuario.nombre_usuario,
                usuario.correo,
                usuario.documento,
                usuario.telefono,
                usuario.fecha_registro,
                usuario.id_estado
            )
        )

        nuevo_id = cursor.fetchone()["id_usuario"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM usuario
            WHERE id_usuario = %s
            RETURNING id_usuario;
        """, (usuario_id,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE usuario
            SET id_rol = %s,
                id_semillero = %s,
                nombre_usuario = %s,
                correo = %s,
                documento = %s,
                telefono = %s,
                fecha_registro = %s,
                id_estado = %s
            WHERE id_usuario = %s
            RETURNING id_usuario;
        """

        cursor.execute(
            query,
            (
                usuario.id_rol,
                usuario.id_semillero,
                usuario.nombre_usuario,
                usuario.correo,
                usuario.documento,
                usuario.telefono,
                usuario.fecha_registro,
                usuario.id_estado,
                usuario_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None