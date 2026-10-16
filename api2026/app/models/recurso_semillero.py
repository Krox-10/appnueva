from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RecursoSemillero(BaseModel):
    id_recurso: Optional[int] = None
    id_semillero: int
    nombre: str
    tipo: str
    cantidad: int = Field(default=1, ge=0)
    descripcion: Optional[str] = None
    estado: bool = True