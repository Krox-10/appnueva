from fastapi import APIRouter, HTTPException

from app.models.modulo import Modulo
from app.repositories.modulo_repo import ModuloRepository


router = APIRouter(
    prefix="/modulos",
    tags=["Gestión de Módulos"]
)

repo = ModuloRepository()


@router.get("/")
def listar_modulos():
    return repo.obtener_todos()


@router.get("/{modulo_id}")
def obtener_modulo(modulo_id: int):
    modulo = repo.obtener_por_id(modulo_id)

    if not modulo:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado"
        )

    return modulo


@router.post("/")
def crear_modulo(modulo: Modulo):
    nuevo_id = repo.crear(modulo)

    return {
        "mensaje": "Módulo registrado exitosamente",
        "id": nuevo_id
    }


@router.delete("/{modulo_id}")
def eliminar_modulo(modulo_id: int):
    exito = repo.eliminar(modulo_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado"
        )

    return {
        "mensaje": "Módulo eliminado correctamente"
    }


@router.put("/{modulo_id}")
def actualizar_modulo(modulo_id: int, modulo: Modulo):
    exito = repo.actualizar(modulo_id, modulo)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado"
        )

    return {
        "mensaje": "Módulo actualizado correctamente"
    }
