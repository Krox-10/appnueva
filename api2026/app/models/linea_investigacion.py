from pydantic import BaseModel
from typing import Optional
from datetime import date

class LineaInvestigacion(BaseModel):
    id_linea: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[date] = None
    id_estado: int