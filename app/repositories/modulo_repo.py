from fastapi import HTTPException
from app.core.database import Database
from app.models.modulo import Modulo


class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                ORDER BY id_modulo ASC;
            """)

            modulos = cursor.fetchall()
            conn.close()

            return modulos

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los módulos"
            )

    def obtener_por_id(self, modulo_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                WHERE id_modulo = %s;
            """, (modulo_id,))

            modulo = cursor.fetchone()
            conn.close()

            if not modulo:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )

            return modulo

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el módulo"
            )

    def crear(self, modulo: Modulo):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulos
                (nombre, descripcion, estado)
                VALUES (%s, %s, %s)
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.nombre,
                    modulo.descripcion,
                    modulo.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_modulo"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el módulo"
            )

    def eliminar(self, modulo_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulos
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """, (modulo_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el módulo"
            )

    def actualizar(self, modulo_id: int, modulo: Modulo):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE modulos
                SET nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.nombre,
                    modulo.descripcion,
                    modulo.estado,
                    modulo_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el módulo"
            )