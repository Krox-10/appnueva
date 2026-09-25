from fastapi import APIRouter, HTTPException
from app.models.reunion import Reunion
from app.repositories.reunion_repo import ReunionRepository

router = APIRouter(prefix="/reuniones", tags=["Gestión de Reuniones"])
repo = ReunionRepository()

@router.get("/")
def listar_reuniones():
    return repo.obtener_todos()

@router.get("/{reunion_id}")
def obtener_reunion(reunion_id: int):
    reunion = repo.obtener_por_id(reunion_id)

    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    return reunion

@router.post("/")
def crear_reunion(reunion: Reunion):
    nuevo_id = repo.crear(reunion)
    return {"mensaje": "Reunión registrada exitosamente", "id": nuevo_id}

@router.delete("/{reunion_id}")
def eliminar_reunion(reunion_id: int):
    exito = repo.eliminar(reunion_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    return {"mensaje": "Reunión eliminada correctamente"}

@router.put("/{reunion_id}")
def actualizar_reunion(reunion_id: int, reunion: Reunion):
    exito = repo.actualizar(reunion_id, reunion)

    if not exito:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    return {"mensaje": "Reunión actualizada correctamente"}