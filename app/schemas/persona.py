from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional

class RolPersonaEnum(str, Enum):
    docente = "docente"
    estudiante = "estudiante"
    director = "director"

class PersonaBase(BaseModel):
    nombreCompleto: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    rol: RolPersonaEnum

class PersonaCrear(PersonaBase):
    pass

class PersonaActualizar(BaseModel):
    nombreCompleto: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol: Optional[RolPersonaEnum] = None

class Persona(PersonaBase):
    id: int = Field(..., alias="idPersona")
    model_config = ConfigDict(from_attributes=True)

