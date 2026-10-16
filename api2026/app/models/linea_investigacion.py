from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LineaInvestigacion(BaseModel):
    id_linea: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True