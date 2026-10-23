from fastapi import HTTPException
from app.core.database import Database
from app.models.usuario import Usuario
from app.core.passwords import hash_password


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None
        try:
            conn = self.db.get_connection()

            if conn is None:
                raise HTTPException(
                    status_code=500,
                    detail="No fue posible conectar con la base de datos"
                )

            cursor = conn.cursor()

            cursor.execute("""
                  SELECT id_usuario, id_rol, id_semillero, nombre_usuario,
                      correo, documento, telefono, estado
                FROM usuario
                ORDER BY id_usuario ASC;
            """)

            return cursor.fetchall()

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los usuarios"
            )
        finally:
            if conn is not None:
                conn.close()

    def obtener_por_id(self, usuario_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            if conn is None:
                raise HTTPException(
                    status_code=500,
                    detail="No fue posible conectar con la base de datos"
                )

            cursor = conn.cursor()

            cursor.execute("""
                  SELECT id_usuario, id_rol, id_semillero, nombre_usuario,
                      correo, documento, telefono, estado
                FROM usuario
                WHERE id_usuario = %s;
            """, (usuario_id,))

            usuario = cursor.fetchone()

            if usuario is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            return usuario

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el usuario"
            )
        finally:
            if conn is not None:
                conn.close()

    def crear(self, usuario: Usuario):
        conn = None
        try:
            conn = self.db.get_connection()

            if conn is None:
                raise HTTPException(
                    status_code=500,
                    detail="No fue posible conectar con la base de datos"
                )

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO usuario (
                    id_rol,
                    id_semillero,
                    nombre_usuario,
                    correo,
                    documento,
                    telefono,
                    estado,
                    contrasena
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario;
            """, (
                usuario.id_rol,
                usuario.id_semillero,
                usuario.nombre_usuario,
                usuario.correo,
                usuario.documento,
                usuario.telefono,
                usuario.estado,
                hash_password(usuario.contrasena)
            ))

            nuevo_usuario = cursor.fetchone()
            conn.commit()

            return nuevo_usuario["id_usuario"]

        except HTTPException:
            if conn is not None:
                conn.rollback()
            raise
        except Exception:
            if conn is not None:
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el usuario. Verifica los datos y sus relaciones."
            )
        finally:
            if conn is not None:
                conn.close()

    def eliminar(self, usuario_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            if conn is None:
                raise HTTPException(
                    status_code=500,
                    detail="No fue posible conectar con la base de datos"
                )

            cursor = conn.cursor()

            # Se desactiva el usuario para conservar sus registros relacionados.
            cursor.execute("""
                UPDATE usuario
                SET estado = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_usuario = %s
                  AND estado = TRUE
                RETURNING id_usuario;
            """, (usuario_id,))

            eliminado = cursor.fetchone()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado o ya inactivo"
                )

            conn.commit()
            return True

        except HTTPException:
            if conn is not None:
                conn.rollback()
            raise
        except Exception:
            if conn is not None:
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error al desactivar el usuario"
            )
        finally:
            if conn is not None:
                conn.close()

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = None
        try:
            conn = self.db.get_connection()

            if conn is None:
                raise HTTPException(
                    status_code=500,
                    detail="No fue posible conectar con la base de datos"
                )

            contrasena_hash = (
                hash_password(usuario.contrasena)
                if usuario.contrasena
                else None
            )

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuario
                SET id_rol = %s,
                    id_semillero = %s,
                    nombre_usuario = %s,
                    correo = %s,
                    documento = %s,
                    telefono = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP,
                    contrasena = COALESCE(%s, contrasena)
                WHERE id_usuario = %s
                RETURNING id_usuario;
            """, (
                usuario.id_rol,
                usuario.id_semillero,
                usuario.nombre_usuario,
                usuario.correo,
                usuario.documento,
                usuario.telefono,
                usuario.estado,
                contrasena_hash,
                usuario_id
            ))

            actualizado = cursor.fetchone()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            conn.commit()
            return True

        except HTTPException:
            if conn is not None:
                conn.rollback()
            raise
        except Exception:
            if conn is not None:
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el usuario. Verifica los datos y sus relaciones."
            )
        finally:
            if conn is not None:
                conn.close()