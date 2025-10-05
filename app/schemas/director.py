from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class DirectorBase(BaseModel):
    idPersona: int
    idPrograma: int

class DirectorCrear(DirectorBase):
    pass

class DirectorActualizar(BaseModel):
    idPersona: Optional[int] = None
    idPrograma: Optional[int] = None

class Director(DirectorBase):
    id: int = Field(..., alias="idDirector")
    model_config = ConfigDict(from_attributes=True)
