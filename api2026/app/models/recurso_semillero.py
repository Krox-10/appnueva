from pydantic import BaseModel
from typing import Optional
from datetime import date

class RecursoSemillero(BaseModel):
    id_recurso: Optional[int] = None
    id_semillero: int
    nombre: str
    tipo: str
    cantidad: int = 1
    descripcion: Optional[str] = None
    id_estado: int
    fecha_registro: Optional[date] = None