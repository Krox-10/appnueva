from pydantic import BaseModel
from typing import Optional
from datetime import date

class Investigacion(BaseModel):
    id_investigacion: Optional[int] = None
    id_semillero: int
    titulo: str
    descripcion: str
    fecha_inicio: date
    fecha_finalizacion: Optional[date] = None
    id_estado: int
    archivo_url: Optional[str] = None