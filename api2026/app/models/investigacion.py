from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Investigacion(BaseModel):
    id_investigacion: Optional[int] = None
    id_semillero: int
    titulo: str
    descripcion: str
    archivo_url: Optional[str] = None
    estado: bool = True