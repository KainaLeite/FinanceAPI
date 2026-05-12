from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import verificar_token
from models.accounts import Conta
from models.transfer import Transferencia
from schemas.transfers import CriarTransferenciaSchema

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("/realizar-transferencia")
async def realizar_transferencia(
    transferencia: CriarTransferenciaSchema,
    usuario=Depends(verificar_token),
    session: Session = Depends(get_db),
):
    if transferencia.conta_origem_id == transferencia.conta_destino_id:
        raise HTTPException(status_code=400, detail="Conta de origem e destino não podem ser iguais.")

    if transferencia.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor da transferência deve ser positivo.")

    conta_origem = session.query(Conta).filter(
        Conta.id == transferencia.conta_origem_id, Conta.user_id == usuario.id
    ).first()
    if not conta_origem:
        raise HTTPException(status_code=404, detail="Conta de origem não encontrada.")

    conta_destino = session.query(Conta).filter(
        Conta.id == transferencia.conta_destino_id, Conta.user_id == usuario.id
    ).first()
    if not conta_destino:
        raise HTTPException(status_code=404, detail="Conta de destino não encontrada.")

    if conta_origem.saldo < transferencia.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente na conta de origem.")

    conta_origem.saldo -= transferencia.valor
    conta_destino.saldo += transferencia.valor

    nova_transferencia = Transferencia(
        conta_origem_id=transferencia.conta_origem_id,
        conta_destino_id=transferencia.conta_destino_id,
        valor=transferencia.valor,
        descricao=transferencia.descricao,
        data=transferencia.data,
        user_id=usuario.id,
    )
    session.add(nova_transferencia)
    session.commit()

    return {"mensagem": f"Transferência de R$ {transferencia.valor:.2f} realizada com sucesso."}


@router.get("/listar-transferencias")
async def listar_transferencias(
    usuario=Depends(verificar_token),
    session: Session = Depends(get_db),
):
    transferencias = session.query(Transferencia).filter(
        Transferencia.user_id == usuario.id
    ).all()
    return transferencias


@router.delete("/deletar-transferencia/{transferencia_id}")
async def deletar_transferencia(
    transferencia_id: int,
    usuario=Depends(verificar_token),
    session: Session = Depends(get_db),
):
    transferencia = session.query(Transferencia).filter(
        Transferencia.id == transferencia_id, Transferencia.user_id == usuario.id
    ).first()
    if not transferencia:
        raise HTTPException(status_code=404, detail="Transferência não encontrada.")

    conta_origem = session.query(Conta).filter(Conta.id == transferencia.conta_origem_id, Conta.user_id == usuario.id).first()
    conta_destino = session.query(Conta).filter(Conta.id == transferencia.conta_destino_id, Conta.user_id == usuario.id).first()

    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Contas da transferência não encontradas, saldos não revertidos.")

    conta_origem.saldo += transferencia.valor
    conta_destino.saldo -= transferencia.valor

    session.delete(transferencia)
    session.commit()
    return {"mensagem": "Transferência deletada e saldos revertidos com sucesso."}
