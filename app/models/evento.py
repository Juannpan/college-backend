from sqlalchemy import Column, Integer, String, Text, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class EventoModel(Base):
    __tablename__ = "evento"

    idEvento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombreEvento = Column(String(200), unique=True)
    descripcion = Column(Text)
    tipo = Column(Enum("academico", "ludico", name="tipo_evento"))
    fecha = Column(Date)
    horaInicio = Column(Time)
    horaFin = Column(Time)
    estado = Column(Enum("registrado", "en revision", "aprobado", "rechazado", name="estado_evento"))
    idInstalacion = Column(Integer, ForeignKey("instalacion.idInstalacion"), nullable=False)
    idResponsable = Column(Integer, ForeignKey("persona.idPersona"), nullable=False)

    instalacion = relationship("InstalacionModel", back_populates="eventos")
    responsable = relationship("PersonaModel", back_populates="eventos_responsable")
    aprobaciones = relationship("AprobacionEventoModel", back_populates="evento")
    participaciones = relationship("ParticipacionModel", back_populates="evento")
    organizaciones_participantes = relationship("OrganizacionParticipacionModel", back_populates="evento")
