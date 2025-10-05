from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class DocenteModel(Base):
    __tablename__ = "docente"

    idPersona = Column(Integer, ForeignKey("persona.idPersona"), primary_key=True)
    codigoDocente = Column(String(10), unique=True)
    idUnidad = Column(Integer, ForeignKey("unidad.idUnidad"), nullable=False)

    persona = relationship("PersonaModel", back_populates="docente")
    unidad = relationship("UnidadModel", back_populates="docentes")
