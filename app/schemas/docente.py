from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class DocenteBase(BaseModel):
    idPersona: int
    idUnidad: int

class DocenteCrear(DocenteBase):
    pass

class DocenteActualizar(BaseModel):
    idPersona: Optional[int] = None
    idUnidad: Optional[int] = None

class Docente(DocenteBase):
    id: int = Field(..., alias="idDocente")
    model_config = ConfigDict(from_attributes=True)
