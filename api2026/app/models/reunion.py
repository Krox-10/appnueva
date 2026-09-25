from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class Reunion(BaseModel):
    id_reunion: Optional[int] = None
    id_semillero: int
    fecha: date
    hora_inicio: time
    hora_fin: Optional[time] = None
    tema: str
    descripcion: Optional[str] = None
    id_estado: int