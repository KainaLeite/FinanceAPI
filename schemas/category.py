from pydantic import BaseModel, ConfigDict
from enum import Enum

class TipoCategoriaSchema(str, Enum):
    receita = "receita"
    despesa = "despesa"

class CriarCategoriaSchema(BaseModel):
    nome: str
    tipo: TipoCategoriaSchema
    cor: str | None = None

class CategoriaRespostaSchema(CriarCategoriaSchema):
    id: int
    user_id: str
    model_config = ConfigDict(from_attributes=True)
        