from fastapi import HTTPException
from app.core.database import Database
from app.models.investigacion_miembro import InvestigacionMiembro


class InvestigacionMiembroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los miembros de investigación"
            )

    def obtener_por_id(self, miembro_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM investigacion_miembro
                WHERE id_investigacion_miembro = %s;
            """, (miembro_id,))

            miembro = cursor.fetchone()
            conn.close()

            if not miembro:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro de investigación no encontrado"
                )

            return miembro

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el miembro de investigación"
            )

    def crear(self, miembro: InvestigacionMiembro):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO investigacion_miembro
                (
                    id_investigacion,
                    id_usuario,
                    rol_investigacion,
                    estado
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
                    miembro.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_investigacion_miembro"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el miembro de investigación"
            )

    def eliminar(self, miembro_id: int):
        try:
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

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro de investigación no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el miembro de investigación"
            )

    def actualizar(
        self,
        miembro_id: int,
        miembro: InvestigacionMiembro
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE investigacion_miembro
                SET id_investigacion = %s,
                    id_usuario = %s,
                    rol_investigacion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_investigacion_miembro = %s
                RETURNING id_investigacion_miembro;
            """

            cursor.execute(
                query,
                (
                    miembro.id_investigacion,
                    miembro.id_usuario,
                    miembro.rol_investigacion,
                    miembro.estado,
                    miembro_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro de investigación no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el miembro de investigación"
            )