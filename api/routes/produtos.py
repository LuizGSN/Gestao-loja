"""
Router para endpoints de produtos.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import DatabaseManager
from api.schemas import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
    Mensagem
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def get_db():
    """Retorna instância do DatabaseManager."""
    from main import app
    return app.state.db


@router.post("/", response_model=Mensagem, status_code=201, summary="Cadastrar novo produto")
async def criar_produto(produto: ProdutoCreate):
    """
    Cadastra um novo produto no sistema.

    - **nome**: Nome do produto (1-60 caracteres)
    - **descricao**: Descrição do produto (1-150 caracteres)
    - **qntd_disponivel**: Quantidade em estoque (≥ 0)
    - **preco**: Preço do produto (≥ 0)
    """
    db = get_db()
    try:
        db.inserir_produto(
            produto.nome,
            produto.descricao,
            produto.qntd_disponivel,
            produto.preco
        )
        logger.info(f"Produto criado via API: {produto.nome}")
        return Mensagem(mensagem="Produto criado com sucesso!", detalhes=produto.nome)
    except Exception as e:
        logger.error(f"Erro ao criar produto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")


@router.get("/", response_model=List[ProdutoResponse], summary="Listar todos os produtos")
async def listar_produtos():
    """
    Retorna todos os produtos cadastrados.
    """
    db = get_db()
    try:
        produtos = db.buscar_todos_produtos()
        return [
            ProdutoResponse(
                id=p[0],
                nome=p[1],
                descricao=p[2],
                qntd_disponivel=p[3],
                preco=float(p[4])
            )
            for p in produtos
        ]
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


@router.get("/{produto_id}", response_model=ProdutoResponse, summary="Buscar produto por ID")
async def buscar_produto(produto_id: int):
    """
    Busca um produto específico pelo ID.
    """
    db = get_db()
    produto = db.buscar_produto_por_id(produto_id)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return ProdutoResponse(
        id=produto[0],
        nome=produto[1],
        descricao=produto[2],
        qntd_disponivel=produto[3],
        preco=float(produto[4])
    )


@router.get("/busca/nome", response_model=List[ProdutoResponse], summary="Buscar produto por nome")
async def buscar_produto_por_nome(nome: str = Query(..., min_length=1, description="Nome ou parte do nome")):
    """
    Busca produtos por nome (busca parcial).
    """
    db = get_db()
    try:
        produtos = db.buscar_produto_por_nome(nome)
        return [
            ProdutoResponse(
                id=p[0],
                nome=p[1],
                descricao=p[2],
                qntd_disponivel=p[3],
                preco=float(p[4])
            )
            for p in produtos
        ]
    except Exception as e:
        logger.error(f"Erro ao buscar produto por nome: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")


@router.get("/busca/faixa-preco", response_model=List[ProdutoResponse], summary="Buscar produto por faixa de preço")
async def buscar_produto_por_preco(
    preco_min: float = Query(..., ge=0, description="Preço mínimo"),
    preco_max: float = Query(..., ge=0, description="Preço máximo")
):
    """
    Busca produtos por faixa de preço.
    """
    if preco_min > preco_max:
        raise HTTPException(status_code=400, detail="Preço mínimo deve ser menor que o máximo")
    
    db = get_db()
    try:
        produtos = db.buscar_produto_por_faixa_preco(preco_min, preco_max)
        return [
            ProdutoResponse(
                id=p[0],
                nome=p[1],
                descricao=p[2],
                qntd_disponivel=p[3],
                preco=float(p[4])
            )
            for p in produtos
        ]
    except Exception as e:
        logger.error(f"Erro ao buscar produto por faixa de preço: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")


@router.put("/{produto_id}", response_model=Mensagem, summary="Atualizar produto")
async def atualizar_produto(produto_id: int, produto: ProdutoUpdate):
    """
    Atualiza um produto existente. Apenas os campos fornecidos serão atualizados.
    """
    db = get_db()
    produto_existente = db.buscar_produto_por_id(produto_id)
    
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    try:
        if produto.nome is not None:
            db.atualizar_nome_produto(produto.nome, produto_id)
        
        if produto.descricao is not None:
            db.atualizar_descricao_produto(produto.descricao, produto_id)
        
        if produto.qntd_disponivel is not None:
            db.atualizar_quantidade_produto(produto.qntd_disponivel, produto_id)
        
        if produto.preco is not None:
            db.atualizar_preco_produto(produto.preco, produto_id)
        
        logger.info(f"Produto {produto_id} atualizado via API")
        return Mensagem(mensagem="Produto atualizado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao atualizar produto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")


@router.delete("/{produto_id}", response_model=Mensagem, summary="Excluir produto")
async def excluir_produto(produto_id: int):
    """
    Exclui um produto pelo ID.
    """
    db = get_db()
    produto = db.buscar_produto_por_id(produto_id)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    try:
        db.excluir_produto(produto_id)
        logger.info(f"Produto {produto_id} excluído via API")
        return Mensagem(mensagem="Produto excluído com sucesso!", detalhes=produto[1])
    except Exception as e:
        logger.error(f"Erro ao excluir produto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir produto: {str(e)}")
