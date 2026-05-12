from sqlalchemy import Column, String, Boolean
from db.base import Base
import uuid
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuario"
    id    = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome  = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    inativo = Column(Boolean, default=False)

    contas = relationship("Conta", back_populates="usuario")