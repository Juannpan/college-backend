from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class FacultadModel(Base):
    __tablename__ = "facultad"

    idFacultad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombreFacultad = Column(String(200), unique=True)
    telefono = Column(String(20))
    idUnidad = Column(Integer, ForeignKey("unidad.idUnidad"), nullable=False)

    unidad = relationship("UnidadModel", back_populates="facultades")
