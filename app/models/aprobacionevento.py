from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base


class AprobacionEventoModel(Base):
    __tablename__ = "aprobacionevento"

    idAprobacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idSecretaria = Column(Integer, ForeignKey("secretariaacademica.idSecretaria"), nullable=False)
    idEvento = Column(Integer, ForeignKey("evento.idEvento"), nullable=False)
    fechaAprobacion = Column(Date)
    actaComite = Column(String(200))
    justificacion = Column(Text)
    avalPDF = Column(String(200))

    secretaria = relationship("SecretariaAcademicaModel", back_populates="aprobaciones")
    evento = relationship("EventoModel", back_populates="aprobaciones")
