from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class InstalacionModel(Base):
    __tablename__ = "instalacion"

    idInstalacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), unique=True)
    capacidad = Column(Integer)
    tipo = Column(Enum("salon", "auditorio", "laboratorio", "cancha", name="tipo_instalacion"))

    eventos = relationship("EventoModel", back_populates="instalacion")
