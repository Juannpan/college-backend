from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class ParticipacionModel(Base):
    __tablename__ = "participacion"

    idParticipacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idPersona = Column(Integer, ForeignKey("persona.idPersona"), nullable=False)
    idEvento = Column(Integer, ForeignKey("evento.idEvento"), nullable=False)
    rolParticipacion = Column(Enum("organizador", "colaborador", "asistente", name="rol_participacion"))

    persona = relationship("PersonaModel", back_populates="participaciones")
    evento = relationship("EventoModel", back_populates="participaciones")
