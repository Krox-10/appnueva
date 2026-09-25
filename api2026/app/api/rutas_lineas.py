from fastapi import APIRouter, HTTPException
from app.models.linea_investigacion import LineaInvestigacion
from app.repositories.linea_investigacion_repo import LineaInvestigacionRepository

router = APIRouter(prefix="/lineas-investigacion", tags=["Gestión de Líneas de Investigación"])
repo = LineaInvestigacionRepository()

@router.get("/")
def listar_lineas():
    return repo.obtener_todos()

@router.get("/{linea_id}")
def obtener_linea(linea_id: int):
    linea = repo.obtener_por_id(linea_id)

    if not linea:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return linea

@router.post("/")
def crear_linea(linea: LineaInvestigacion):
    nuevo_id = repo.crear(linea)
    return {"mensaje": "Línea registrada exitosamente", "id": nuevo_id}

@router.delete("/{linea_id}")
def eliminar_linea(linea_id: int):
    exito = repo.eliminar(linea_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return {"mensaje": "Línea eliminada correctamente"}

@router.put("/{linea_id}")
def actualizar_linea(linea_id: int, linea: LineaInvestigacion):
    exito = repo.actualizar(linea_id, linea)

    if not exito:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return {"mensaje": "Línea actualizada correctamente"}