from pydantic import BaseModel
from datetime import date


class CriarMetaSchema(BaseModel):
    nome: str
    valor_alvo: float
    valor_atual: float = 0.0
    data_limite: date | None = None


class AtualizarMetaSchema(BaseModel):
    nome: str
    valor_alvo: float
    valor_atual: float
    data_limite: date | None = None
