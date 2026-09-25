from fastapi import APIRouter, HTTPException
from app.models.semillero import Semillero
from app.repositories.semillero_repo import SemilleroRepository

router = APIRouter(prefix="/semilleros", tags=["Gestión de Semilleros"])
repo = SemilleroRepository()

@router.get("/")
def listar_semilleros():
    return repo.obtener_todos()

@router.get("/{semillero_id}")
def obtener_semillero(semillero_id: int):
    semillero = repo.obtener_por_id(semillero_id)

    if not semillero:
        raise HTTPException(status_code=404, detail="Semillero no encontrado")

    return semillero

@router.post("/")
def crear_semillero(semillero: Semillero):
    nuevo_id = repo.crear(semillero)
    return {"mensaje": "Semillero registrado exitosamente", "id": nuevo_id}

@router.delete("/{semillero_id}")
def eliminar_semillero(semillero_id: int):
    exito = repo.eliminar(semillero_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Semillero no encontrado")

    return {"mensaje": "Semillero eliminado correctamente"}

@router.put("/{semillero_id}")
def actualizar_semillero(semillero_id: int, semillero: Semillero):
    exito = repo.actualizar(semillero_id, semillero)

    if not exito:
        raise HTTPException(status_code=404, detail="Semillero no encontrado")

    return {"mensaje": "Semillero actualizado correctamente"}