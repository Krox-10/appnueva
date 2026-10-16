from fastapi import APIRouter, HTTPException
from app.models.modulo_x_rol import ModuloXRol
from app.repositories.modulo_x_rol_repo import ModuloXRolRepository


router = APIRouter(
    prefix="/modulos-x-rol",
    tags=["Gestión de Módulos por Rol"]
)

repo = ModuloXRolRepository()


@router.get("/")
def listar_modulos_x_rol():
    return repo.obtener_todos()


@router.get("/rol/{id_rol}")
def obtener_modulos_por_rol(id_rol: int):
    from app.core.database import Database

    db = Database()
    conn = db.get_connection()

    if conn is None:
        raise HTTPException(
            status_code=500,
            detail="No fue posible conectar con la base de datos"
        )

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.id_modulo,
                m.nombre
            FROM modulosxrol mxr
            INNER JOIN modulos m
                ON m.id_modulo = mxr.id_modulo
            WHERE mxr.id_rol = %s
              AND mxr.estado = TRUE
              AND m.estado = TRUE
            ORDER BY m.id_modulo;
        """, (id_rol,))

        return cursor.fetchall()

    finally:
        conn.close()


@router.get("/{moduloxrol_id}")
def obtener_modulo_x_rol(moduloxrol_id: int):
    registro = repo.obtener_por_id(moduloxrol_id)

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return registro


@router.post("/")
def crear_modulo_x_rol(moduloxrol: ModuloXRol):
    nuevo_id = repo.crear(moduloxrol)

    return {
        "mensaje": "Módulo asignado al rol exitosamente",
        "id": nuevo_id
    }


@router.delete("/{moduloxrol_id}")
def eliminar_modulo_x_rol(moduloxrol_id: int):
    exito = repo.eliminar(moduloxrol_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Asignación eliminada correctamente"
    }


@router.put("/{moduloxrol_id}")
def actualizar_modulo_x_rol(
    moduloxrol_id: int,
    moduloxrol: ModuloXRol
):
    exito = repo.actualizar(moduloxrol_id, moduloxrol)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Asignación actualizada correctamente"
    }