from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class FacultadBase(BaseModel):
    nombreFacultad: str = Field(..., min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    idUnidad: int

class FacultadCrear(FacultadBase):
    pass

class FacultadActualizar(BaseModel):
    nombreFacultad: Optional[str] = None
    telefono: Optional[str] = None
    idUnidad: Optional[int] = None

class Facultad(FacultadBase):
    id: int = Field(..., alias="idFacultad")
    model_config = ConfigDict(from_attributes=True)
