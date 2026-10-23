from fastapi import HTTPException
from app.core.database import Database
from app.models.reunion import Reunion


class ReunionRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM reunion
                ORDER BY id_reunion ASC;
            """)

            reuniones = cursor.fetchall()
            conn.close()
            return reuniones

        except Exception as e:
            print("Error al obtener las reuniones:", e)
            raise HTTPException(
                status_code=500,
                detail="Error al obtener las reuniones"
            )

    def obtener_por_id(self, reunion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM reunion
                WHERE id_reunion = %s;
            """, (reunion_id,))

            reunion = cursor.fetchone()
            conn.close()

            if not reunion:
                raise HTTPException(
                    status_code=404,
                    detail="Reunión no encontrada"
                )

            return reunion

        except HTTPException:
            raise
        except Exception as e:
            print("Error al obtener la reunión:", e)
            raise HTTPException(
                status_code=500,
                detail="Error al obtener la reunión"
            )

    def crear(self, reunion: Reunion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO reunion (
                    id_semillero,
                    fecha,
                    hora_inicio,
                    hora_fin,
                    tema,
                    descripcion,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_reunion;
            """

            cursor.execute(query, (
                reunion.id_semillero,
                reunion.fecha,
                reunion.hora_inicio,
                reunion.hora_fin,
                reunion.tema,
                reunion.descripcion,
                reunion.estado
            ))

            nuevo_id = cursor.fetchone()["id_reunion"]
            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print("Error real al registrar la reunión:", e)

            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass

            raise HTTPException(
                status_code=500,
                detail="Error al registrar la reunión"
            )

    def eliminar(self, reunion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM reunion
                WHERE id_reunion = %s
                RETURNING id_reunion;
            """, (reunion_id,))

            eliminado = cursor.fetchone()
            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Reunión no encontrada"
                )

            return True

        except HTTPException:
            raise
        except Exception as e:
            print("Error al eliminar la reunión:", e)
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la reunión"
            )

    def actualizar(self, reunion_id: int, reunion: Reunion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE reunion
                SET id_semillero = %s,
                    fecha = %s,
                    hora_inicio = %s,
                    hora_fin = %s,
                    tema = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_reunion = %s
                RETURNING id_reunion;
            """

            cursor.execute(query, (
                reunion.id_semillero,
                reunion.fecha,
                reunion.hora_inicio,
                reunion.hora_fin,
                reunion.tema,
                reunion.descripcion,
                reunion.estado,
                reunion_id
            ))

            actualizado = cursor.fetchone()
            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Reunión no encontrada"
                )

            return True

        except HTTPException:
            raise
        except Exception as e:
            print("Error real al actualizar la reunión:", e)

            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass

            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la reunión"
            )