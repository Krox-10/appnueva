from fastapi import HTTPException
from app.core.database import Database
from app.models.recurso_semillero import RecursoSemillero


class RecursoSemilleroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM recurso_semillero
                ORDER BY id_recurso ASC;
            """)

            recursos = cursor.fetchall()
            conn.close()

            return recursos

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los recursos"
            )

    def obtener_por_id(self, recurso_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM recurso_semillero
                WHERE id_recurso = %s;
            """, (recurso_id,))

            recurso = cursor.fetchone()
            conn.close()

            if not recurso:
                raise HTTPException(
                    status_code=404,
                    detail="Recurso no encontrado"
                )

            return recurso

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el recurso"
            )

    def crear(self, recurso: RecursoSemillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO recurso_semillero
                (
                    id_semillero,
                    nombre,
                    tipo,
                    cantidad,
                    descripcion,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_recurso;
            """

            cursor.execute(
                query,
                (
                    recurso.id_semillero,
                    recurso.nombre,
                    recurso.tipo,
                    recurso.cantidad,
                    recurso.descripcion,
                    recurso.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_recurso"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el recurso"
            )

    def eliminar(self, recurso_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM recurso_semillero
                WHERE id_recurso = %s
                RETURNING id_recurso;
            """, (recurso_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Recurso no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el recurso"
            )

    def actualizar(self, recurso_id: int, recurso: RecursoSemillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE recurso_semillero
                SET id_semillero = %s,
                    nombre = %s,
                    tipo = %s,
                    cantidad = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_recurso = %s
                RETURNING id_recurso;
            """

            cursor.execute(
                query,
                (
                    recurso.id_semillero,
                    recurso.nombre,
                    recurso.tipo,
                    recurso.cantidad,
                    recurso.descripcion,
                    recurso.estado,
                    recurso_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Recurso no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el recurso"
            )