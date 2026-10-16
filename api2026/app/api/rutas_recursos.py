from fastapi import APIRouter, HTTPException

from app.models.recurso_semillero import RecursoSemillero
from app.repositories.recurso_semillero_repo import RecursoSemilleroRepository


router = APIRouter(
    prefix="/recursos-semillero",
    tags=["Gestión de Recursos de Semillero"]
)

repo = RecursoSemilleroRepository()


@router.get("/")
def listar_recursos():
    return repo.obtener_todos()


@router.get("/{recurso_id}")
def obtener_recurso(recurso_id: int):
    recurso = repo.obtener_por_id(recurso_id)

    if not recurso:
        raise HTTPException(
            status_code=404,
            detail="Recurso no encontrado"
        )

    return recurso


@router.post("/")
def crear_recurso(recurso: RecursoSemillero):
    nuevo_id = repo.crear(recurso)

    return {
        "mensaje": "Recurso registrado exitosamente",
        "id": nuevo_id
    }


@router.delete("/{recurso_id}")
def eliminar_recurso(recurso_id: int):
    exito = repo.eliminar(recurso_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Recurso no encontrado"
        )

    return {
        "mensaje": "Recurso eliminado correctamente"
    }


@router.put("/{recurso_id}")
def actualizar_recurso(
    recurso_id: int,
    recurso: RecursoSemillero
):
    exito = repo.actualizar(recurso_id, recurso)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Recurso no encontrado"
        )

    return {
        "mensaje": "Recurso actualizado correctamente"
    }