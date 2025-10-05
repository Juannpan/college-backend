from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class DirectorModel(Base):
    __tablename__ = "director"

    idPersona = Column(Integer, ForeignKey("persona.idPersona"), primary_key=True)
    tipo = Column(Enum("academico", "programa", name="tipo_director"))

    persona = relationship("PersonaModel", back_populates="director")
