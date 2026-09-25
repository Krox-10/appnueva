from fastapi import APIRouter, HTTPException
from app.models.producto_investigacion import ProductoInvestigacion
from app.repositories.producto_investigacion_repo import ProductoInvestigacionRepository

router = APIRouter(prefix="/productos-investigacion", tags=["Gestión de Productos de Investigación"])
repo = ProductoInvestigacionRepository()

@router.get("/")
def listar_productos():
    return repo.obtener_todos()

@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    producto = repo.obtener_por_id(producto_id)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto

@router.post("/")
def crear_producto(producto: ProductoInvestigacion):
    nuevo_id = repo.crear(producto)
    return {"mensaje": "Producto registrado exitosamente", "id": nuevo_id}

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    exito = repo.eliminar(producto_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto eliminado correctamente"}

@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    producto: ProductoInvestigacion
):
    exito = repo.actualizar(producto_id, producto)

    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto actualizado correctamente"}