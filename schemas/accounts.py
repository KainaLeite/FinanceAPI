from pydantic import BaseModel, ConfigDict
from enum import Enum


class TipoContaSchema(str, Enum):
    CORRENTE = "corrente"
    POUPANCA = "poupanca"
    CARTEIRA = "carteira"
    DIGITAL = "digital"


class CriaContaSchema(BaseModel):
    nome: str
    tipo: TipoContaSchema
    saldo: float

    model_config = ConfigDict(from_attributes=True)


class AtualizarContaSchema(BaseModel):
    nome: str
    tipo: TipoContaSchema

    model_config = ConfigDict(from_attributes=True)