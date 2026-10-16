from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Semillero(BaseModel):
    id_semillero: Optional[int] = None
    id_linea: int
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True