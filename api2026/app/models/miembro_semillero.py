from pydantic import BaseModel
from typing import Optional
from datetime import date

class MiembroSemillero(BaseModel):
    id_miembro: Optional[int] = None
    id_usuario: int
    id_semillero: int
    fecha_ingreso: Optional[date] = None
    cargo: Optional[str] = None
    estado: str = "Activo"