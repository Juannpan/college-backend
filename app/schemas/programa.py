from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProgramaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    idUnidad: int

class ProgramaCrear(ProgramaBase):
    pass

class ProgramaActualizar(BaseModel):
    nombre: Optional[str] = None
    idUnidad: Optional[int] = None

class Programa(ProgramaBase):
    id: int = Field(..., alias="idPrograma")
    model_config = ConfigDict(from_attributes=True)
