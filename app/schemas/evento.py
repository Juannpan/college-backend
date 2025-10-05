from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date, time

# Definimos enums compatibles con Pydantic/JSON (str + Enum)
class TipoEventoEnum(str, Enum):
    academico = "academico"
    ludico = "ludico"

class EstadoEventoEnum(str, Enum):
    registrado = "registrado"
    en_revision = "en revision"
    aprobado = "aprobado"
    rechazado = "rechazado"

class EventoBase(BaseModel):
    nombreEvento: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo: TipoEventoEnum
    fecha: date
    horaInicio: time
    horaFin: time
    estado: EstadoEventoEnum
    idInstalacion: int
    idResponsable: int

class EventoCrear(EventoBase):
    pass

class EventoActualizar(BaseModel):
    nombreEvento: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[TipoEventoEnum] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFin: Optional[time] = None
    estado: Optional[EstadoEventoEnum] = None
    idInstalacion: Optional[int] = None
    idResponsable: Optional[int] = None

class Evento(EventoBase):
    # Usamos alias para mapear la propiedad ORM idEvento a la respuesta 'id'
    id: int = Field(..., alias="idEvento")
    model_config = ConfigDict(from_attributes=True)

