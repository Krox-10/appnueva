from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductoInvestigacion(BaseModel):
    id_producto: Optional[int] = None
    id_investigacion: int
    titulo: str
    tipo: str
    descripcion: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    archivo_url: Optional[str] = None