from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: int
    id_semillero: Optional[int] = None
    nombre_usuario: str
    correo: str
    documento: str
    telefono: Optional[str] = None
    estado: bool = True
    contrasena: Optional[str] = None