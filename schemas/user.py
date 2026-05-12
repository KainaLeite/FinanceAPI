from pydantic import BaseModel, UUID4, ConfigDict, field_validator


def validar_email(email: str) -> str:
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Email inválido.")
    return email


class CriarUsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

    @field_validator("email")
    @classmethod
    def email_valido(cls, valor):
        return validar_email(valor)


class LoginSchema(BaseModel):
    email: str
    senha: str

class UsuarioRespostaSchema(BaseModel):    
    email: str
    nome:str 
    id: UUID4
    model_config = ConfigDict(from_attributes=True)

class AtualizarUsuarioSchema(BaseModel):
    nome: str
    email: str

    @field_validator("email")
    @classmethod
    def email_valido(cls, valor):
        return validar_email(valor)


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TrocarSenhaSchema(BaseModel):
    senha_atual: str
    nova_senha: str        

    model_config = ConfigDict(from_attributes=True)