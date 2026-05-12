from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, DateTime
from db.base import Base
from datetime import datetime, timezone


class Transacao (Base):
     __tablename__ = "transacao"
     id = Column(Integer, primary_key=True, autoincrement= True)
     tipo = Column(String, nullable=False)
     descricao = Column(String)
     categoria_id = Column(Integer, ForeignKey("categoria.id"))
     data = Column(Date)
     valor = Column(Float)
     user_id = Column(String, ForeignKey("usuario.id"))
     created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
     conta_id = Column(String, ForeignKey("conta.id"))
