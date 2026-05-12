from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SAEnum
from db.base import Base
from schemas.category import TipoCategoriaSchema


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    tipo = Column(SAEnum(TipoCategoriaSchema), nullable=False)
    cor = Column(String)
    user_id = Column(String, ForeignKey("usuario.id"))