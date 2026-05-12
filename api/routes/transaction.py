from fastapi import APIRouter, Depends, HTTPException
from schemas.transaction import CriarTransacaoSchema
from sqlalchemy.orm import Session
from db.session import get_db
from models.transaction import Transacao
from models.accounts import Conta
from models.category import Categoria
from core.security import verificar_token

router = APIRouter(prefix="/transaction", tags=["transaction"])


def _aplicar_saldo(conta: Conta, tipo: str, valor: float):
    if tipo == "entrada":
        conta.saldo += valor
    else:
        conta.saldo -= valor


def _reverter_saldo(conta: Conta, tipo: str, valor: float):
    if tipo == "entrada":
        conta.saldo -= valor
    else:
        conta.saldo += valor


@router.post("/criar-transacao")
async def criar_transacao(transacao: CriarTransacaoSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    conta = session.query(Conta).filter(Conta.id == transacao.conta_id, Conta.user_id == usuario.id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")

    categoria = session.query(Categoria).filter(Categoria.id == transacao.categoria_id, Categoria.user_id == usuario.id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    nova_transacao = Transacao(
        valor=transacao.valor,
        descricao=transacao.descricao,
        tipo=transacao.tipo,
        user_id=usuario.id,
        data=transacao.data,
        categoria_id=transacao.categoria_id,
        conta_id=transacao.conta_id,
    )
    _aplicar_saldo(conta, transacao.tipo, transacao.valor)
    session.add(nova_transacao)
    session.commit()
    return {"mensagem": f"Transação criada com sucesso: {transacao.descricao}"}


@router.get("/listar-transacoes")
async def listar_transacoes(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    transacoes = session.query(Transacao).filter(Transacao.user_id == usuario.id).all()
    return transacoes


@router.delete("/deletar-transacao/{transacao_id}")
async def deletar_transacao(transacao_id: int, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    transacao = session.query(Transacao).filter(Transacao.id == transacao_id, Transacao.user_id == usuario.id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    conta = session.query(Conta).filter(Conta.id == transacao.conta_id, Conta.user_id == usuario.id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta da transação não encontrada.")

    _reverter_saldo(conta, transacao.tipo, transacao.valor)
    session.delete(transacao)
    session.commit()
    return {"mensagem": "Transação deletada com sucesso"}


@router.put("/atualizar-transacao/{transacao_id}")
async def atualizar_transacao(transacao_id: int, transacao_atualizada: CriarTransacaoSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    transacao = session.query(Transacao).filter(Transacao.id == transacao_id, Transacao.user_id == usuario.id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    conta_antiga = session.query(Conta).filter(Conta.id == transacao.conta_id, Conta.user_id == usuario.id).first()
    if not conta_antiga:
        raise HTTPException(status_code=404, detail="Conta da transação não encontrada.")

    nova_conta = session.query(Conta).filter(Conta.id == transacao_atualizada.conta_id, Conta.user_id == usuario.id).first()
    if not nova_conta:
        raise HTTPException(status_code=404, detail="Nova conta não encontrada.")

    nova_categoria = session.query(Categoria).filter(Categoria.id == transacao_atualizada.categoria_id, Categoria.user_id == usuario.id).first()
    if not nova_categoria:
        raise HTTPException(status_code=404, detail="Nova categoria não encontrada.")

    _reverter_saldo(conta_antiga, transacao.tipo, transacao.valor)
    _aplicar_saldo(nova_conta, transacao_atualizada.tipo, transacao_atualizada.valor)

    transacao.valor = transacao_atualizada.valor
    transacao.descricao = transacao_atualizada.descricao
    transacao.tipo = transacao_atualizada.tipo
    transacao.data = transacao_atualizada.data
    transacao.categoria_id = transacao_atualizada.categoria_id
    transacao.conta_id = transacao_atualizada.conta_id
    session.commit()
    return {"mensagem": "Transação atualizada com sucesso"}
