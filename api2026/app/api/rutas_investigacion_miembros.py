from fastapi import APIRouter, HTTPException
from app.models.investigacion_miembro import InvestigacionMiembro
from app.repositories.investigacion_miembro_repo import InvestigacionMiembroRepository

router = APIRouter(prefix="/investigaciones-miembros", tags=["Gestión de Miembros de Investigaciones"])
repo = InvestigacionMiembroRepository()

@router.get("/")
def listar_registros():
    return repo.obtener_todos()

@router.get("/{registro_id}")
def obtener_registro(registro_id: int):
    registro = repo.obtener_por_id(registro_id)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro

@router.post("/")
def crear_registro(registro: InvestigacionMiembro):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Registro creado exitosamente", "id": nuevo_id}

@router.delete("/{registro_id}")
def eliminar_registro(registro_id: int):
    exito = repo.eliminar(registro_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

@router.put("/{registro_id}")
def actualizar_registro(
    registro_id: int,
    registro: InvestigacionMiembro
):
    exito = repo.actualizar(registro_id, registro)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}