from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Rol(BaseModel):
    id_rol: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True