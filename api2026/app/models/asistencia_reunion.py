from pydantic import BaseModel
from typing import Optional

class AsistenciaReunion(BaseModel):
    id_asistencia: Optional[int] = None
    id_reunion: int
    id_usuario: int
    asistio: bool = False
    observacion: Optional[str] = None