from pydantic import BaseModel
from typing import Optional
from datetime import date

class Semillero(BaseModel):
    id_semillero: Optional[int] = None
    id_linea: int
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[date] = None
    id_estado: int