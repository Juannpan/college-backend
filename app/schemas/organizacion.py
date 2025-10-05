from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class OrganizacionBase(BaseModel):
    nombreOrganizacion: str = Field(..., min_length=1, max_length=200)
    representanteLegal: str = Field(..., min_length=1, max_length=200)
    ubicacion: str = Field(..., min_length=1, max_length=200)
    sectorEconomico: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)

class OrganizacionCrear(OrganizacionBase):
    pass

class OrganizacionActualizar(BaseModel):
    nombreOrganizacion: Optional[str] = None
    representanteLegal: Optional[str] = None
    ubicacion: Optional[str] = None
    sectorEconomico: Optional[str] = None
    telefono: Optional[str] = None

class Organizacion(OrganizacionBase):
    id: int = Field(..., alias="idOrganizacion")
    model_config = ConfigDict(from_attributes=True)
