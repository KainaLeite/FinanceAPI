from pydantic import BaseModel, ConfigDict
from datetime import date


class CriarTransferenciaSchema(BaseModel):
    conta_origem_id: str
    conta_destino_id: str
    valor: float
    descricao: str | None = None
    data: date


class ListarTransferenciaSchema(CriarTransferenciaSchema):
    id: int
    user_id: str

    model_config = ConfigDict(from_attributes=True)
