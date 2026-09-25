from fastapi import APIRouter, HTTPException
from app.models.investigacion import Investigacion
from app.repositories.investigacion_repo import InvestigacionRepository

router = APIRouter(prefix="/investigaciones", tags=["Gestión de Investigaciones"])
repo = InvestigacionRepository()

@router.get("/")
def listar_investigaciones():
    return repo.obtener_todos()

@router.get("/{investigacion_id}")
def obtener_investigacion(investigacion_id: int):
    investigacion = repo.obtener_por_id(investigacion_id)

    if not investigacion:
        raise HTTPException(status_code=404, detail="Investigación no encontrada")

    return investigacion

@router.post("/")
def crear_investigacion(investigacion: Investigacion):
    nuevo_id = repo.crear(investigacion)
    return {"mensaje": "Investigación registrada exitosamente", "id": nuevo_id}

@router.delete("/{investigacion_id}")
def eliminar_investigacion(investigacion_id: int):
    exito = repo.eliminar(investigacion_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Investigación no encontrada")

    return {"mensaje": "Investigación eliminada correctamente"}

@router.put("/{investigacion_id}")
def actualizar_investigacion(
    investigacion_id: int,
    investigacion: Investigacion
):
    exito = repo.actualizar(investigacion_id, investigacion)

    if not exito:
        raise HTTPException(status_code=404, detail="Investigación no encontrada")

    return {"mensaje": "Investigación actualizada correctamente"}