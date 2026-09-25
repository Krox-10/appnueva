from fastapi import APIRouter, HTTPException
from app.models.miembro_semillero import MiembroSemillero
from app.repositories.miembro_semillero_repo import MiembroSemilleroRepository

router = APIRouter(prefix="/miembros-semilleros", tags=["Gestión de Miembros de Semilleros"])
repo = MiembroSemilleroRepository()

@router.get("/")
def listar_miembros():
    return repo.obtener_todos()

@router.get("/{miembro_id}")
def obtener_miembro(miembro_id: int):
    miembro = repo.obtener_por_id(miembro_id)

    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    return miembro

@router.post("/")
def crear_miembro(miembro: MiembroSemillero):
    nuevo_id = repo.crear(miembro)
    return {"mensaje": "Miembro registrado exitosamente", "id": nuevo_id}

@router.delete("/{miembro_id}")
def eliminar_miembro(miembro_id: int):
    exito = repo.eliminar(miembro_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    return {"mensaje": "Miembro eliminado correctamente"}

@router.put("/{miembro_id}")
def actualizar_miembro(miembro_id: int, miembro: MiembroSemillero):
    exito = repo.actualizar(miembro_id, miembro)

    if not exito:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    return {"mensaje": "Miembro actualizado correctamente"}