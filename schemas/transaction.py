from pydantic import BaseModel, ConfigDict
from datetime import date
from enum import Enum


class TipoTransacaoEnum(str, Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"


class CriarTransacaoSchema(BaseModel):
    valor: float
    tipo: TipoTransacaoEnum
    descricao: str | None = None
    categoria_id: int
    conta_id: str
    data: date

class ListarTransacaoSchema(CriarTransacaoSchema):
    id : int
    created_at : date
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)