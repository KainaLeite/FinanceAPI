from fastapi import APIRouter, Depends, HTTPException
from schemas.category import CriarCategoriaSchema
from sqlalchemy.orm import Session
from db.session import get_db
from models.category import Categoria
from models.transaction import Transacao
from core.security import verificar_token


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.post("/criar-categoria")
async def criar_categoria(criar_categoria: CriarCategoriaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    categoria_existente = session.query(Categoria).filter(
        Categoria.nome == criar_categoria.nome, Categoria.user_id == usuario.id
    ).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="Já existe uma categoria com esse nome.")

    nova_categoria = Categoria(
        nome=criar_categoria.nome,
        tipo=criar_categoria.tipo,
        cor = criar_categoria.cor,
        user_id=usuario.id
    )
    session.add(nova_categoria)
    session.commit()
    session.refresh(nova_categoria)
    return {"mensagem": f"Categoria criada com sucesso: {criar_categoria.nome}"}

@router.get("/listar-categoria")
async def listar_categoria(usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    categorias = session.query(Categoria).filter(Categoria.user_id == usuario.id).all()
    return categorias

@router.put("/atualizar-categoria/{categoria_id}")
async def atualizar_categoria(categoria_id: int, criar_categoria: CriarCategoriaSchema, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    categoria = session.query(Categoria).filter(Categoria.id == categoria_id, Categoria.user_id == usuario.id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categoria.nome = criar_categoria.nome
    categoria.tipo = criar_categoria.tipo
    categoria.cor = criar_categoria.cor
    session.commit()
    return {"mensagem": f"Categoria atualizada com sucesso: {criar_categoria.nome}"}    

@router.delete("/deletar-categoria/{categoria_id}")
async def deletar_categoria(categoria_id: int, usuario=Depends(verificar_token), session: Session = Depends(get_db)):
    categoria = session.query(Categoria).filter(Categoria.id == categoria_id, Categoria.user_id == usuario.id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    transacao_vinculada = session.query(Transacao).filter(Transacao.categoria_id == categoria_id).first()
    if transacao_vinculada:
        raise HTTPException(status_code=400, detail="Não é possível deletar a categoria pois ela possui transações vinculadas.")

    session.delete(categoria)
    session.commit()
    return {"mensagem": f"Categoria deletada com sucesso: {categoria.nome}"}