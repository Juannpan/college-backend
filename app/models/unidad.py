from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class UnidadModel(Base):
    __tablename__ = "unidad"

    idUnidad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), unique=True)

    docentes = relationship("DocenteModel", back_populates="unidad")
    programas = relationship("ProgramaModel", back_populates="unidad")
    facultades = relationship("FacultadModel", back_populates="unidad")
    secretarias = relationship("SecretariaAcademicaModel", back_populates="unidad")
