from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import verificar_token
from models.goal import Meta
from schemas.goals import CriarMetaSchema, AtualizarMetaSchema

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/criar-meta")
async def criar_meta(meta: CriarMetaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    nova_meta = Meta(
        nome=meta.nome,
        valor_alvo=meta.valor_alvo,
        valor_atual=meta.valor_atual,
        data_limite=meta.data_limite,
        user_id=usuario.id,
    )
    session.add(nova_meta)
    session.commit()
    session.refresh(nova_meta)
    return {"mensagem": f"Meta criada com sucesso: {meta.nome}"}


@router.get("/listar-metas")
async def listar_metas(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    metas = session.query(Meta).filter(Meta.user_id == usuario.id).all()
    return metas


@router.put("/atualizar-meta/{meta_id}")
async def atualizar_meta(meta_id: int, meta_atualizada: AtualizarMetaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    meta = session.query(Meta).filter(Meta.id == meta_id, Meta.user_id == usuario.id).first()
    if not meta:
        raise HTTPException(status_code=404, detail="Meta não encontrada.")
    meta.nome = meta_atualizada.nome
    meta.valor_alvo = meta_atualizada.valor_alvo
    meta.valor_atual = meta_atualizada.valor_atual
    meta.data_limite = meta_atualizada.data_limite
    session.commit()
    return {"mensagem": f"Meta atualizada com sucesso: {meta.nome}"}


@router.delete("/deletar-meta/{meta_id}")
async def deletar_meta(meta_id: int, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    meta = session.query(Meta).filter(Meta.id == meta_id, Meta.user_id == usuario.id).first()
    if not meta:
        raise HTTPException(status_code=404, detail="Meta não encontrada.")
    session.delete(meta)
    session.commit()
    return {"mensagem": f"Meta deletada com sucesso: {meta.nome}"}
