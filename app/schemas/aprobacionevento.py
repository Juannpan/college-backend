from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class AprobacionEventoBase(BaseModel):
    idSecretaria: int
    idEvento: int
    fechaAprobacion: date
    actaComite: Optional[str] = Field(None, max_length=200)
    justificacion: Optional[str] = None
    avalPDF: Optional[str] = Field(None, max_length=200)

class AprobacionEventoCrear(AprobacionEventoBase):
    pass

class AprobacionEventoActualizar(BaseModel):
    idSecretaria: Optional[int] = None
    idEvento: Optional[int] = None
    fechaAprobacion: Optional[date] = None
    actaComite: Optional[str] = None
    justificacion: Optional[str] = None
    avalPDF: Optional[str] = None

class AprobacionEvento(AprobacionEventoBase):
    id: int = Field(..., alias="idAprobacion")
    model_config = ConfigDict(from_attributes=True)
