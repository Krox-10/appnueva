from pydantic import BaseModel
from typing import Optional
from datetime import date

class InvestigacionMiembro(BaseModel):
    id_investigacion_miembro: Optional[int] = None
    id_investigacion: int
    id_usuario: int
    rol_investigacion: str
    fecha_vinculacion: Optional[date] = None