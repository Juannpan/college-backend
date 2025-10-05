from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class EstadoContrasenaEnum(str, Enum):
    activa = "activa"
    inactiva = "inactiva"

class HistorialContrasenasBase(BaseModel):
    idPersona: int
    contrasena: str = Field(..., min_length=6, max_length=200)
    fechaCambio: datetime
    estado: EstadoContrasenaEnum = EstadoContrasenaEnum.activa

class HistorialContrasenasCrear(HistorialContrasenasBase):
    pass

class HistorialContrasenasActualizar(BaseModel):
    idPersona: Optional[int] = None
    contrasena: Optional[str] = None
    fechaCambio: Optional[datetime] = None
    estado: Optional[EstadoContrasenaEnum] = None

class HistorialContrasenas(HistorialContrasenasBase):
    id: int = Field(..., alias="idHistorial")
    model_config = ConfigDict(from_attributes=True)


