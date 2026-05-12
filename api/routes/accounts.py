from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import verificar_token
from models.accounts import Conta
from models.transaction import Transacao
from models.transfer import Transferencia
from schemas.accounts import CriaContaSchema, AtualizarContaSchema

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.post("/criar-conta")
async def criar_conta(conta: CriaContaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    conta_existente = session.query(Conta).filter(Conta.nome == conta.nome, Conta.user_id == usuario.id).first()
    if conta_existente:
        raise HTTPException(status_code=400, detail="Já existe uma conta com esse nome para este usuário.")
    nova_conta = Conta(
        nome=conta.nome,
        tipo=conta.tipo,
        saldo=conta.saldo,
        user_id=usuario.id
        
    )   
    session.add(nova_conta)
    session.commit()
    session.refresh(nova_conta)
    return {"mensagem": f"Conta criada com sucesso: {conta.nome}"}


@router.get("/listar-contas")
async def listar_contas(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    contas = session.query(Conta).filter(Conta.user_id == usuario.id).all()
    return contas



@router.put("/atualizar-conta/{conta_id}")
async def atualizar_conta(conta_id: str, conta_atualizada: AtualizarContaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    conta = session.query(Conta).filter(Conta.id == conta_id, Conta.user_id == usuario.id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    conta.nome = conta_atualizada.nome
    conta.tipo = conta_atualizada.tipo
    session.commit()
    return {"mensagem": f"Conta atualizada com sucesso: {conta.nome}"}


@router.delete("/deletar-conta/{conta_id}")
async def deletar_conta(conta_id: str, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    conta = session.query(Conta).filter(Conta.id == conta_id, Conta.user_id == usuario.id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")

    transacao_vinculada = session.query(Transacao).filter(Transacao.conta_id == conta_id).first()
    transferencia_vinculada = session.query(Transferencia).filter(
        (Transferencia.conta_origem_id == conta_id) | (Transferencia.conta_destino_id == conta_id)
    ).first()

    if transacao_vinculada or transferencia_vinculada:
        raise HTTPException(
            status_code=400,
            detail="Não é possível deletar a conta pois ela possui transações ou transferências vinculadas."
        )

    session.delete(conta)
    session.commit()
    return {"mensagem": f"Conta deletada com sucesso: {conta.nome}"}
