from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class RolParticipacionEnum(str, Enum):
    organizador = "organizador"
    colaborador = "colaborador"
    asistente = "asistente"

class ParticipacionBase(BaseModel):
    idPersona: int
    idEvento: int
    rolParticipacion: RolParticipacionEnum

class ParticipacionCrear(ParticipacionBase):
    pass

class ParticipacionActualizar(BaseModel):
    idPersona: Optional[int] = None
    idEvento: Optional[int] = None
    rolParticipacion: Optional[RolParticipacionEnum] = None

class Participacion(ParticipacionBase):
    id: int = Field(..., alias="idParticipacion")
    model_config = ConfigDict(from_attributes=True)

