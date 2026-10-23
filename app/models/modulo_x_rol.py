from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ModuloXRol(BaseModel):
    id_moduloxrol: Optional[int] = None
    id_rol: int
    id_modulo: int
    estado: bool = True