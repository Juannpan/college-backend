from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# Definimos enum para el tipo de instalación
class TipoInstalacionEnum(str, Enum):
    salon = "salon"
    auditorio = "auditorio"
    laboratorio = "laboratorio"
    cancha = "cancha"

class InstalacionBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    capacidad: Optional[int] = None
    tipo: TipoInstalacionEnum

class InstalacionCrear(InstalacionBase):
    pass

class InstalacionActualizar(BaseModel):
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    tipo: Optional[TipoInstalacionEnum] = None

class Instalacion(InstalacionBase):
    id: int = Field(..., alias="idInstalacion")
    model_config = ConfigDict(from_attributes=True)

