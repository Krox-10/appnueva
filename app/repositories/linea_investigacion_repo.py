from fastapi import HTTPException
from app.core.database import Database
from app.models.linea_investigacion import LineaInvestigacion


class LineaInvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener las líneas de investigación"
            )

    def obtener_por_id(self, linea_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM linea_investigacion
                WHERE id_linea = %s;
            """, (linea_id,))

            linea = cursor.fetchone()
            conn.close()

            if not linea:
                raise HTTPException(
                    status_code=404,
                    detail="Línea de investigación no encontrada"
                )

            return linea

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener la línea de investigación"
            )

    def crear(self, linea: LineaInvestigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO linea_investigacion
                (nombre, descripcion, estado)
                VALUES (%s, %s, %s)
                RETURNING id_linea;
            """

            cursor.execute(
                query,
                (
                    linea.nombre,
                    linea.descripcion,
                    linea.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_linea"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar la línea de investigación"
            )

    def eliminar(self, linea_id: int):
        try:
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

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Línea de investigación no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la línea de investigación"
            )

    def actualizar(self, linea_id: int, linea: LineaInvestigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE linea_investigacion
                SET nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_linea = %s
                RETURNING id_linea;
            """

            cursor.execute(
                query,
                (
                    linea.nombre,
                    linea.descripcion,
                    linea.estado,
                    linea_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Línea de investigación no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la línea de investigación"
            )