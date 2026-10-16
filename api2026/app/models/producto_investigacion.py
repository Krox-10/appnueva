from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoInvestigacion(BaseModel):
    id_producto: Optional[int] = None
    id_investigacion: int
    titulo: str
    tipo: str
    descripcion: Optional[str] = None
    archivo_url: Optional[str] = None
    estado: bool = True