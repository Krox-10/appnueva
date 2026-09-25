from app.core.database import Database
from app.models.producto_investigacion import ProductoInvestigacion

class ProductoInvestigacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
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

    def obtener_por_id(self, producto_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM producto_investigacion
            WHERE id_producto = %s;
        """, (producto_id,))

        producto = cursor.fetchone()
        conn.close()

        return producto

    def crear(self, producto: ProductoInvestigacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO producto_investigacion
            (
                id_investigacion,
                titulo,
                tipo,
                descripcion,
                fecha_publicacion,
                archivo_url
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
                producto.fecha_publicacion,
                producto.archivo_url
            )
        )

        nuevo_id = cursor.fetchone()["id_producto"]

        conn.commit()
        conn.close()

        return nuevo_id

    def eliminar(self, producto_id: int):
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

        return eliminado is not None

    def actualizar(
        self,
        producto_id: int,
        producto: ProductoInvestigacion
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE producto_investigacion
            SET id_investigacion = %s,
                titulo = %s,
                tipo = %s,
                descripcion = %s,
                fecha_publicacion = %s,
                archivo_url = %s
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
                producto.fecha_publicacion,
                producto.archivo_url,
                producto_id
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado is not None