import uuid
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime, timezone


class Transferencia(Base):
    __tablename__ = "transferencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conta_origem_id = Column(String, ForeignKey("conta.id"), nullable=False)
    conta_destino_id = Column(String, ForeignKey("conta.id"), nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String)
    data = Column(Date)
    user_id = Column(String, ForeignKey("usuario.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
