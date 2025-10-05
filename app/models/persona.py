from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class PersonaModel(Base):
    __tablename__ = "persona"

    idPersona = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombreCompleto = Column(String(200))
    email = Column(String(200), unique=True)
    telefono = Column(String(20))
    rol = Column(Enum("docente", "estudiante", "director", name="rol_persona"))

    historial_contrasenas = relationship("HistorialContrasenasModel", back_populates="persona", cascade="all, delete-orphan")
    eventos_responsable = relationship("EventoModel", back_populates="responsable")
    participaciones = relationship("ParticipacionModel", back_populates="persona")

    director = relationship("DirectorModel", back_populates="persona", uselist=False)
    docente = relationship("DocenteModel", back_populates="persona", uselist=False)
    estudiante = relationship("EstudianteModel", back_populates="persona", uselist=False)


