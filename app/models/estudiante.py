from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class EstudianteModel(Base):
    __tablename__ = "estudiante"

    idPersona = Column(Integer, ForeignKey("persona.idPersona"), primary_key=True)
    codigoEstudiante = Column(String(10), unique=True)
    idPrograma = Column(Integer, ForeignKey("programa.idPrograma"))

    persona = relationship("PersonaModel", back_populates="estudiante")
    programa = relationship("ProgramaModel", back_populates="estudiantes")
