from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class EsRepresentanteLegalEnum(str, Enum):
    si = "si"
    no = "no"


class OrganizacionParticipacionBase(BaseModel):
    idEvento: int
    idOrganizacion: int
    esRepresentanteLegal: EsRepresentanteLegalEnum
    certificadoParticipacion: Optional[str] = Field(None, max_length=200)
    nombreParticipanteSustituto: Optional[str] = Field(None, max_length=200)


class OrganizacionParticipacionCrear(OrganizacionParticipacionBase):
    pass


class OrganizacionParticipacionActualizar(BaseModel):
    idEvento: Optional[int] = None
    idOrganizacion: Optional[int] = None
    esRepresentanteLegal: Optional[EsRepresentanteLegalEnum] = None
    certificadoParticipacion: Optional[str] = None
    nombreParticipanteSustituto: Optional[str] = None


class OrganizacionParticipacion(OrganizacionParticipacionBase):
    id: int = Field(..., alias="idParticipacionExterna")
    model_config = ConfigDict(from_attributes=True)


