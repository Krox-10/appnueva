from fastapi import HTTPException
from app.core.database import Database
from app.models.modulo_x_rol import ModuloXRol


class ModuloXRolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulosxrol
                ORDER BY id_moduloxrol ASC;
            """)

            registros = cursor.fetchall()
            conn.close()

            return registros

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los registros"
            )

    def obtener_por_id(self, moduloxrol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulosxrol
                WHERE id_moduloxrol = %s;
            """, (moduloxrol_id,))

            registro = cursor.fetchone()
            conn.close()

            if not registro:
                raise HTTPException(
                    status_code=404,
                    detail="Registro no encontrado"
                )

            return registro

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el registro"
            )

    def crear(self, moduloxrol: ModuloXRol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulosxrol
                (id_rol, id_modulo, estado)
                VALUES (%s, %s, %s)
                RETURNING id_moduloxrol;
            """

            cursor.execute(
                query,
                (
                    moduloxrol.id_rol,
                    moduloxrol.id_modulo,
                    moduloxrol.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_moduloxrol"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el registro"
            )

    def eliminar(self, moduloxrol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulosxrol
                WHERE id_moduloxrol = %s
                RETURNING id_moduloxrol;
            """, (moduloxrol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Registro no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el registro"
            )

    def actualizar(self, moduloxrol_id: int, moduloxrol: ModuloXRol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE modulosxrol
                SET id_rol = %s,
                    id_modulo = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_moduloxrol = %s
                RETURNING id_moduloxrol;
            """

            cursor.execute(
                query,
                (
                    moduloxrol.id_rol,
                    moduloxrol.id_modulo,
                    moduloxrol.estado,
                    moduloxrol_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Registro no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el registro"
            )