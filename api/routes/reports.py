from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.session import get_db
from core.security import verificar_token
from models.transaction import Transacao
from models.accounts import Conta
from models.category import Categoria

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/resumo")
async def resumo(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    saldo_total = session.query(func.sum(Conta.saldo)).filter(Conta.user_id == usuario.id).scalar() or 0.0
    total_entradas = session.query(func.sum(Transacao.valor)).filter(Transacao.user_id == usuario.id, Transacao.tipo == "entrada").scalar() or 0.0
    total_saidas = session.query(func.sum(Transacao.valor)).filter(Transacao.user_id == usuario.id, Transacao.tipo == "saida").scalar() or 0.0

    return {
        "saldo_total": saldo_total,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
    }


@router.get("/por-categoria")
async def relatorio_por_categoria(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    resultados = (
        session.query(Categoria.nome, func.sum(Transacao.valor))
        .outerjoin(Transacao, Transacao.categoria_id == Categoria.id)
        .filter(Categoria.user_id == usuario.id)
        .group_by(Categoria.nome)
        .all()
    )

    return [{"categoria": nome, "total": total or 0.0} for nome, total in resultados]
