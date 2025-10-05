from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class EstudianteBase(BaseModel):
    idPersona: int
    idPrograma: int
    semestre: int = Field(..., ge=1, le=12)

class EstudianteCrear(EstudianteBase):
    pass

class EstudianteActualizar(BaseModel):
    idPersona: Optional[int] = None
    idPrograma: Optional[int] = None
    semestre: Optional[int] = None

class Estudiante(EstudianteBase):
    id: int = Field(..., alias="idEstudiante")
    model_config = ConfigDict(from_attributes=True)
