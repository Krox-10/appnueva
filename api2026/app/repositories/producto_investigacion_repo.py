from fastapi import HTTPException
from app.core.database import Database
from app.models.producto_investigacion import ProductoInvestigacion


class ProductoInvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM producto_investigacion
                ORDER BY id_producto ASC;
            """)

            productos = cursor.fetchall()
            conn.close()

            return productos

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los productos"
            )

    def obtener_por_id(self, producto_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM producto_investigacion
                WHERE id_producto = %s;
            """, (producto_id,))

            producto = cursor.fetchone()
            conn.close()

            if not producto:
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )

            return producto

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el producto"
            )

    def crear(self, producto: ProductoInvestigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO producto_investigacion
                (
                    id_investigacion,
                    titulo,
                    tipo,
                    descripcion,
                    archivo_url,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_producto;
            """

            cursor.execute(
                query,
                (
                    producto.id_investigacion,
                    producto.titulo,
                    producto.tipo,
                    producto.descripcion,
                    producto.archivo_url,
                    producto.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_producto"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el producto"
            )

    def eliminar(self, producto_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM producto_investigacion
                WHERE id_producto = %s
                RETURNING id_producto;
            """, (producto_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el producto"
            )

    def actualizar(self, producto_id: int, producto: ProductoInvestigacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE producto_investigacion
                SET id_investigacion = %s,
                    titulo = %s,
                    tipo = %s,
                    descripcion = %s,
                    archivo_url = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_producto = %s
                RETURNING id_producto;
            """

            cursor.execute(
                query,
                (
                    producto.id_investigacion,
                    producto.titulo,
                    producto.tipo,
                    producto.descripcion,
                    producto.archivo_url,
                    producto.estado,
                    producto_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el producto"
            )