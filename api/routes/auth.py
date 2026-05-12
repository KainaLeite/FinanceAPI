from fastapi import APIRouter, Depends, HTTPException
from schemas.user import CriarUsuarioSchema, LoginSchema, TrocarSenhaSchema, RefreshTokenSchema
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import Usuario
from fastapi.security import OAuth2PasswordRequestForm
from core.security import (
    hash_senha,
    verificar_senha,
    criar_token,
    autenticar_usuario,
    verificar_token,
)
from jose import jwt, JWTError
from core.config import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

    
@router.post("/registrar")
async def registrar(criar_usuario: CriarUsuarioSchema, session: Session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email == criar_usuario.email).first()

    # Email já existe e está ativo — bloqueia
    if usuario and not usuario.inativo:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado")

    senha_criptografada = hash_senha(str(criar_usuario.senha))
    
    # Email existe mas está inativo — reativa
    if usuario and usuario.inativo:
        usuario.inativo = False
        usuario.nome = criar_usuario.nome
        usuario.senha = senha_criptografada
        session.commit()
        return {"mensagem": f"Conta reativada com sucesso: {criar_usuario.email}"}
    
    # Email não existe — cria novo
    novo_usuario = Usuario(
        nome=criar_usuario.nome,
        email=criar_usuario.email,
        senha=senha_criptografada,
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuário cadastrado com sucesso: {criar_usuario.email}"}


@router.post("/login")
async def login(login_schema: LoginSchema, session=Depends(get_db)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(
            status_code=400, detail="Credenciais inválidas ou Usuário inválido"
        )
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=60 * 24 * 7)
    usuario.refresh_token = refresh_token
    session.commit()
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh")
async def refresh(refresh_schema: RefreshTokenSchema, session=Depends(get_db)):
    try:
        dic_info = jwt.decode(refresh_schema.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = str(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario or usuario.refresh_token != refresh_schema.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    novo_access_token = criar_token(usuario.id)
    return {"access_token": novo_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(usuario=Depends(verificar_token), session=Depends(get_db)):
    usuario.refresh_token = None
    session.commit()
    return {"mensagem": "Logout realizado com sucesso"}



@router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session=Depends(get_db)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas ou Usuário inválido")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }



@router.delete("/deletar-conta")
async def deletar_conta(usuario=Depends(verificar_token), session=Depends(get_db)):
    usuario.refresh_token = None
    usuario.inativo = True
    session.commit()
    return {"mensagem": "Conta deletada com sucesso"}


@router.post("/trocar-senha")
async def trocar_senha(trocar_senha_schema: TrocarSenhaSchema, usuario=Depends(verificar_token), session=Depends(get_db)):
    if not verificar_senha(trocar_senha_schema.senha_atual, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    nova_senha_criptografada = hash_senha(str(trocar_senha_schema.nova_senha))
    usuario.senha = nova_senha_criptografada
    session.commit()
    return {"mensagem": "Senha trocada com sucesso"}