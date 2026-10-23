from fastapi import HTTPException
from app.core.database import Database
from app.models.investigacion import Investigacion


class InvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener las investigaciones"
            )

    def obtener_por_id(self, investigacion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM investigacion
                WHERE id_investigacion = %s;
            """, (investigacion_id,))

            investigacion = cursor.fetchone()
            conn.close()

            if not investigacion:
                raise HTTPException(
                    status_code=404,
                    detail="Investigación no encontrada"
                )

            return investigacion

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener la investigación"
            )

    def crear(self, investigacion: Investigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO investigacion
                (
                    id_semillero,
                    titulo,
                    descripcion,
                    archivo_url,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_investigacion;
            """

            cursor.execute(
                query,
                (
                    investigacion.id_semillero,
                    investigacion.titulo,
                    investigacion.descripcion,
                    investigacion.archivo_url,
                    investigacion.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_investigacion"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar la investigación"
            )

    def eliminar(self, investigacion_id: int):
        try:
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

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Investigación no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la investigación"
            )

    def actualizar(self, investigacion_id: int, investigacion: Investigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE investigacion
                SET id_semillero = %s,
                    titulo = %s,
                    descripcion = %s,
                    archivo_url = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_investigacion = %s
                RETURNING id_investigacion;
            """

            cursor.execute(
                query,
                (
                    investigacion.id_semillero,
                    investigacion.titulo,
                    investigacion.descripcion,
                    investigacion.archivo_url,
                    investigacion.estado,
                    investigacion_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Investigación no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la investigación"
            )