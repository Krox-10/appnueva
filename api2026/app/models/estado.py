from pydantic import BaseModel
from typing import Optional

class Estado(BaseModel):
    id_estado: Optional[int] = None
    nombre: str
    categoria: str
    descripcion: Optional[str] = None