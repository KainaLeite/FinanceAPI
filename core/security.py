import bcrypt as _bcrypt
from datetime import datetime, timedelta, timezone
from models.user import Usuario
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError
from db.session import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import oauth2_schema

def hash_senha(senha: str) -> str:
    return _bcrypt.hashpw(senha.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")

def verificar_senha(senha: str, hashed: str) -> bool:
    return _bcrypt.checkpw(senha.encode("utf-8"), hashed.encode("utf-8"))

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not verificar_senha(senha, usuario.senha):
        return False
    if usuario.inativo:
        return False
    return usuario
   

    
def criar_token(id_usuario, duracao_token=ACCESS_TOKEN_EXPIRE_MINUTES):
    data_de_expiração = datetime.now(timezone.utc) + timedelta(minutes=duracao_token)
    dic_informações = {"sub": str(id_usuario), "exp": data_de_expiração}
    jwt_codificado = jwt.encode(dic_informações, SECRET_KEY, ALGORITHM)
    return jwt_codificado    


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = str(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário inválido")
    if usuario.inativo:
        raise HTTPException(status_code=401, detail="Usuário inativo")

    return usuario




    