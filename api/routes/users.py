from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import verificar_token
from models.user import Usuario
from schemas.user import UsuarioRespostaSchema, AtualizarUsuarioSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/perfil", response_model=UsuarioRespostaSchema)
async def perfil(usuario=Depends(verificar_token)):
    return usuario


@router.put("/atualizar-perfil")
async def atualizar_perfil(usuario_atualizado: AtualizarUsuarioSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    email_existente = session.query(Usuario).filter(Usuario.email == usuario_atualizado.email, Usuario.id != usuario.id).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="Email já está em uso por outro usuário.")
    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email
    session.commit()
    return {"mensagem": "Perfil atualizado com sucesso"}
