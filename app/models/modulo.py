from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Modulo(BaseModel):
    id_modulo: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True