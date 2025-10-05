from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class HistorialContrasenasModel(Base):
    __tablename__ = "historialcontrasenas"

    idHistorial = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idPersona = Column(Integer, ForeignKey("persona.idPersona"), nullable=False)

    # En la BD la columna se llama 'contrasena' (varchar(200))
    contrasena = Column(String(200), nullable=False)

    fechaCambio = Column(DateTime, nullable=False)

    # Enum tal cual la tabla: ('activa','inactiva')
    estado = Column(Enum("activa", "inactiva"), nullable=False, default="activa")

    # IMPORTANTE: Ya NO declaramos 'esVigente' porque no existe en la tabla
    persona = relationship("PersonaModel", back_populates="historial_contrasenas")


