from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class UnidadBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)

class UnidadCrear(UnidadBase):
    pass

class UnidadActualizar(BaseModel):
    nombre: Optional[str] = None

class Unidad(UnidadBase):
    id: int = Field(..., alias="idUnidad")
    model_config = ConfigDict(from_attributes=True)
