from fastapi import HTTPException
from app.core.database import Database
from app.models.asistencia_reunion import AsistenciaReunion


class AsistenciaReunionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM asistencia_reunion
                ORDER BY id_asistencia ASC;
            """)

            asistencias = cursor.fetchall()
            conn.close()

            return asistencias

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener las asistencias"
            )

    def obtener_por_id(self, asistencia_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM asistencia_reunion
                WHERE id_asistencia = %s;
            """, (asistencia_id,))

            asistencia = cursor.fetchone()
            conn.close()

            if not asistencia:
                raise HTTPException(
                    status_code=404,
                    detail="Asistencia no encontrada"
                )

            return asistencia

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener la asistencia"
            )

    def crear(self, asistencia: AsistenciaReunion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO asistencia_reunion
                (
                    id_reunion,
                    id_usuario,
                    asistio,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_asistencia;
            """

            cursor.execute(
                query,
                (
                    asistencia.id_reunion,
                    asistencia.id_usuario,
                    asistencia.asistio,
                    asistencia.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_asistencia"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar la asistencia"
            )

    def eliminar(self, asistencia_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM asistencia_reunion
                WHERE id_asistencia = %s
                RETURNING id_asistencia;
            """, (asistencia_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Asistencia no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la asistencia"
            )

    def actualizar(
        self,
        asistencia_id: int,
        asistencia: AsistenciaReunion
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE asistencia_reunion
                SET id_reunion = %s,
                    id_usuario = %s,
                    asistio = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_asistencia = %s
                RETURNING id_asistencia;
            """

            cursor.execute(
                query,
                (
                    asistencia.id_reunion,
                    asistencia.id_usuario,
                    asistencia.asistio,
                    asistencia.estado,
                    asistencia_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Asistencia no encontrada"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la asistencia"
            )