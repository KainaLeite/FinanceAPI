from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from db.base import Base


class Meta(Base):
    __tablename__ = "meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    valor_alvo = Column(Float, nullable=False)
    valor_atual = Column(Float, default=0.0)
    data_limite = Column(Date, nullable=True)
    user_id = Column(String, ForeignKey("usuario.id"))
