from fastapi import HTTPException
from app.core.database import Database
from app.models.semillero import Semillero


class SemilleroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM semillero
                ORDER BY id_semillero ASC;
            """)

            semilleros = cursor.fetchall()
            conn.close()

            return semilleros

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los semilleros"
            )

    def obtener_por_id(self, semillero_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM semillero
                WHERE id_semillero = %s;
            """, (semillero_id,))

            semillero = cursor.fetchone()
            conn.close()

            if not semillero:
                raise HTTPException(
                    status_code=404,
                    detail="Semillero no encontrado"
                )

            return semillero

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el semillero"
            )

    def crear(self, semillero: Semillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO semillero
                (id_linea, nombre, descripcion, estado)
                VALUES (%s, %s, %s, %s)
                RETURNING id_semillero;
            """

            cursor.execute(
                query,
                (
                    semillero.id_linea,
                    semillero.nombre,
                    semillero.descripcion,
                    semillero.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_semillero"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el semillero"
            )

    def eliminar(self, semillero_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM semillero
                WHERE id_semillero = %s
                RETURNING id_semillero;
            """, (semillero_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Semillero no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el semillero"
            )

    def actualizar(self, semillero_id: int, semillero: Semillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE semillero
                SET id_linea = %s,
                    nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_semillero = %s
                RETURNING id_semillero;
            """

            cursor.execute(
                query,
                (
                    semillero.id_linea,
                    semillero.nombre,
                    semillero.descripcion,
                    semillero.estado,
                    semillero_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Semillero no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el semillero"
            )