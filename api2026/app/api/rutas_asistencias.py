from fastapi import APIRouter, HTTPException
from app.models.asistencia_reunion import AsistenciaReunion
from app.repositories.asistencia_reunion_repo import AsistenciaReunionRepository

router = APIRouter(prefix="/asistencias", tags=["Gestión de Asistencias"])
repo = AsistenciaReunionRepository()

@router.get("/")
def listar_asistencias():
    return repo.obtener_todos()

@router.get("/{asistencia_id}")
def obtener_asistencia(asistencia_id: int):
    asistencia = repo.obtener_por_id(asistencia_id)

    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return asistencia

@router.post("/")
def crear_asistencia(asistencia: AsistenciaReunion):
    nuevo_id = repo.crear(asistencia)
    return {"mensaje": "Asistencia registrada exitosamente", "id": nuevo_id}

@router.delete("/{asistencia_id}")
def eliminar_asistencia(asistencia_id: int):
    exito = repo.eliminar(asistencia_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    return {"mensaje": "Asistencia eliminada correctamente"}

@router.put("/{asistencia_id}")
def actualizar_asistencia(
    asistencia_id: int,
    asistencia: AsistenciaReunion
):
    exito = repo.actualizar(asistencia_id, asistencia)

    if not exito:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    return {"mensaje": "Asistencia actualizada correctamente"}