from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class OrganizacionModel(Base):
    __tablename__ = "organizacion"

    idOrganizacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombreOrganizacion = Column(String(200), unique=True)
    representanteLegal = Column(String(200))
    ubicacion = Column(String(200))
    sectorEconomico = Column(String(200))
    telefono = Column(String(20))

    participaciones = relationship("OrganizacionParticipacionModel", back_populates="organizacion")
