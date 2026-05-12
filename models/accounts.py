import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Conta(Base):
    __tablename__ = "conta"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    saldo = Column(Float, default=0)
    tipo = Column(String)  # corrente, poupanca, carteira

    user_id = Column(String, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="contas")