from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class SecretariaAcademicaModel(Base):
    __tablename__ = "secretariaacademica"

    idSecretaria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idUnidad = Column(Integer, ForeignKey("unidad.idUnidad"), nullable=False)
    nombreSecretaria = Column(String(200), unique=True)

    unidad = relationship("UnidadModel", back_populates="secretarias")
    aprobaciones = relationship("AprobacionEventoModel", back_populates="secretaria")
