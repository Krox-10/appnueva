from fastapi import HTTPException
from app.core.database import Database
from app.models.rol import Rol


class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los roles"
            )

    def obtener_por_id(self, rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol
                WHERE id_rol = %s;
            """, (rol_id,))

            rol = cursor.fetchone()
            conn.close()

            if not rol:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )

            return rol

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el rol"
            )

    def crear(self, rol: Rol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO rol
                (nombre, descripcion, estado)
                VALUES (%s, %s, %s)
                RETURNING id_rol;
            """

            cursor.execute(
                query,
                (
                    rol.nombre,
                    rol.descripcion,
                    rol.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_rol"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el rol"
            )

    def eliminar(self, rol_id: int):
        try:
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

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el rol"
            )

    def actualizar(self, rol_id: int, rol: Rol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE rol
                SET nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_rol = %s
                RETURNING id_rol;
            """

            cursor.execute(
                query,
                (
                    rol.nombre,
                    rol.descripcion,
                    rol.estado,
                    rol_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el rol"
            )