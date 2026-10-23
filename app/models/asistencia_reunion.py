from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AsistenciaReunion(BaseModel):
    id_asistencia: Optional[int] = None
    id_reunion: int
    id_usuario: int
    asistio: Optional[bool] = None
    estado: bool = True