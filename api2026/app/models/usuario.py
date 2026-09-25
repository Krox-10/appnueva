from pydantic import BaseModel
from typing import Optional
from datetime import date

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: int
    id_semillero: Optional[int] = None
    nombre_usuario: str
    correo: str
    documento: str
    telefono: Optional[str] = None
    fecha_registro: Optional[date] = None
    id_estado: int = 1