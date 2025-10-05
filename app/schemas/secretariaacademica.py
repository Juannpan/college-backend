from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SecretariaAcademicaBase(BaseModel):
    idPersona: int
    idFacultad: int

class SecretariaAcademicaCrear(SecretariaAcademicaBase):
    pass

class SecretariaAcademicaActualizar(BaseModel):
    idPersona: Optional[int] = None
    idFacultad: Optional[int] = None

class SecretariaAcademica(SecretariaAcademicaBase):
    id: int = Field(..., alias="idSecretariaAcademica")
    model_config = ConfigDict(from_attributes=True)
