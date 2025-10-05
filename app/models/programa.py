from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class ProgramaModel(Base):
    __tablename__ = "programa"

    idPrograma = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idUnidad = Column(Integer, ForeignKey("unidad.idUnidad"), nullable=False)
    nombre = Column(String(200), unique=True)

    unidad = relationship("UnidadModel", back_populates="programas")
    estudiantes = relationship("EstudianteModel", back_populates="programa")
