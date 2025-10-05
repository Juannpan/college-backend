from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class OrganizacionParticipacionModel(Base):
    __tablename__ = "organizacionparticipacion"

    idParticipacionExterna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idEvento = Column(Integer, ForeignKey("evento.idEvento"), nullable=False)
    idOrganizacion = Column(Integer, ForeignKey("organizacion.idOrganizacion"), nullable=False)
    # Enum alineado con la BD
    esRepresentanteLegal = Column(Enum("si", "no", name="es_representante_legal"), nullable=False)
    certificadoParticipacion = Column(String(200))
    nombreParticipanteSustituto = Column(String(200))

    evento = relationship("EventoModel", back_populates="organizaciones_participantes")
    organizacion = relationship("OrganizacionModel", back_populates="participaciones")


