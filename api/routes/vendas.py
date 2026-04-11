"""
Router para endpoints de vendas.
"""

from fastapi import APIRouter, HTTPException, Query, Request, Depends
from typing import List, Optional
from datetime import date, datetime
from database import DatabaseManager
from api.schemas import (
    VendaCreate,
    VendaUpdate,
    VendaResponse,
    ResumoVendas,
    Mensagem
)
from api.dependencies import get_db, parse_data_venda
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.post("/", response_model=Mensagem, status_code=201, summary="Registrar nova venda")
async def criar_venda(venda: VendaCreate, db: DatabaseManager = Depends(get_db)):
    """
    Registra uma nova venda com controle automático de estoque.

    - **id_produto**: ID do produto vendido
    - **qntd_vendida**: Quantidade vendida
    - **data_venda**: Data da venda (opcional, usa data atual)
    """
    # Verificar se produto existe
    produto = db.buscar_produto_por_id(venda.id_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verificar estoque
    qntd_disponivel = produto[3]
    if qntd_disponivel <= 0:
        raise HTTPException(status_code=400, detail="Produto sem estoque")

    if venda.qntd_vendida > qntd_disponivel:
        raise HTTPException(
            status_code=400,
            detail=f"Quantidade vendida ({venda.qntd_vendida}) excede a disponível ({qntd_disponivel})"
        )

    # Usar data atual se não fornecida
    data_venda = venda.data_venda or datetime.now().date()
    data_venda_str = data_venda.strftime("%Y-%m-%d")

    try:
        db.iniciar_transacao()
        try:
            # Registrar venda (sem auto_commit)
            db.registrar_venda(venda.id_produto, venda.qntd_vendida, data_venda_str, auto_commit=False)

            # Atualizar estoque de forma atômica (previne race condition)
            rows_afetadas = db.vender_produto(venda.id_produto, venda.qntd_vendida)

            if rows_afetadas == 0:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail="Estoque insuficiente. Outro cliente pode ter comprado o último item."
                )

            nova_qntd = qntd_disponivel - venda.qntd_vendida
            db.commit()

            logger.info(f"Venda registrada via API: {venda.qntd_vendida}x {produto[1]}")
            return Mensagem(
                mensagem="Venda registrada com sucesso!",
                detalhes=f"Produto: {produto[1]}, Estoque restante: {nova_qntd}"
            )
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar venda: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar venda: {str(e)}")


@router.get("/", response_model=List[VendaResponse], summary="Listar todas as vendas")
async def listar_vendas(db: DatabaseManager = Depends(get_db)):
    """
    Retorna todas as vendas registradas.
    """
    try:
        vendas = db.buscar_todas_vendas()
        return [
            VendaResponse(
                id=v[0],
                produto_nome=v[1],
                qntd_vendida=v[2],
                data_venda=parse_data_venda(v[3])
            )
            for v in vendas
        ]
    except Exception as e:
        logger.error(f"Erro ao listar vendas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar vendas: {str(e)}")


@router.get("/{venda_id}", response_model=VendaResponse, summary="Buscar venda por ID")
async def buscar_venda(venda_id: int, db: DatabaseManager = Depends(get_db)):
    """
    Busca uma venda específica pelo ID.
    """
    venda = db.buscar_venda_por_id(venda_id)

    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    return VendaResponse(
        id=venda[0],
        produto_nome=venda[1],
        qntd_vendida=venda[2],
        data_venda=parse_data_venda(venda[3])
    )


@router.get("/relatorio/periodo", response_model=ResumoVendas, summary="Relatório de vendas por período")
async def relatorio_vendas(
    data_inicio: Optional[date] = Query(None, description="Data inicial do filtro"),
    data_fim: Optional[date] = Query(None, description="Data final do filtro"),
    db: DatabaseManager = Depends(get_db)
):
    """
    Gera relatório de vendas por período com resumo.
    """
    # Usar padrões se não fornecidos
    if not data_inicio:
        data_inicio = datetime.strptime("2000-01-01", "%Y-%m-%d").date()
    if not data_fim:
        data_fim = datetime.now().date()

    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
    data_fim_str = data_fim.strftime("%Y-%m-%d")

    try:
        vendas = db.buscar_vendas_por_periodo(data_inicio_str, data_fim_str)

        if not vendas:
            return ResumoVendas(
                total_vendas=0,
                total_itens_vendidos=0,
                vendas=[]
            )

        vendas_response = [
            VendaResponse(
                id=v[0],
                produto_nome=v[1],
                qntd_vendida=v[2],
                data_venda=parse_data_venda(v[3])
            )
            for v in vendas
        ]

        total_vendas = len(vendas)
        total_itens = sum(v[2] for v in vendas)

        return ResumoVendas(
            total_vendas=total_vendas,
            total_itens_vendidos=total_itens,
            vendas=vendas_response
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de vendas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")


@router.put("/{venda_id}", response_model=Mensagem, summary="Atualizar venda")
async def atualizar_venda(venda_id: int, venda: VendaUpdate, db: DatabaseManager = Depends(get_db)):
    """
    Atualiza uma venda existente.
    """
    venda_existente = db.buscar_venda_por_id(venda_id)

    if not venda_existente:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    try:
        # Preparar dados antes da transação
        produto_id = None
        estoque_real = None
        nova_qntd = None
        nova_data = None

        if venda.qntd_vendida is not None:
            produto_id = db.buscar_id_produto_da_venda(venda_id)
            if not produto_id:
                raise HTTPException(status_code=404, detail="Produto da venda não encontrado")

            produto = db.buscar_produto_por_id(produto_id)
            qntd_estoque_atual = produto[3]
            qntd_atual_venda = venda_existente[2]

            estoque_real = qntd_estoque_atual + qntd_atual_venda

            if venda.qntd_vendida > estoque_real:
                raise HTTPException(
                    status_code=400,
                    detail=f"Quantidade excede o estoque disponível ({estoque_real})"
                )
            nova_qntd = venda.qntd_vendida

        if venda.data_venda is not None:
            nova_data = venda.data_venda.strftime("%Y-%m-%d")

        # Executar tudo dentro de uma única transação
        if nova_qntd is not None or nova_data is not None:
            db.iniciar_transacao()
            try:
                if nova_qntd is not None:
                    db.atualizar_quantidade_venda(nova_qntd, venda_id, auto_commit=False)
                    db.atualizar_quantidade_produto(estoque_real - nova_qntd, produto_id, auto_commit=False)

                if nova_data is not None:
                    db.atualizar_data_venda(nova_data, venda_id, auto_commit=False)

                db.commit()
            except Exception:
                db.rollback()
                raise

        logger.info(f"Venda {venda_id} atualizada via API")
        return Mensagem(mensagem="Venda atualizada com sucesso!")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar venda: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar venda: {str(e)}")


@router.delete("/{venda_id}", response_model=Mensagem, summary="Excluir venda")
async def excluir_venda(venda_id: int, db: DatabaseManager = Depends(get_db)):
    """
    Exclui uma venda e devolve o estoque.
    """
    venda = db.buscar_venda_por_id(venda_id)

    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    try:
        db.iniciar_transacao()
        try:
            # Obter produto da venda
            produto_id = db.buscar_id_produto_da_venda(venda_id)
            if not produto_id:
                raise Exception("Produto da venda não encontrado")

            produto = db.buscar_produto_por_id(produto_id)
            novo_estoque = produto[3] + venda[2]

            # Devolver estoque (sem auto_commit)
            db.atualizar_quantidade_produto(novo_estoque, produto_id, auto_commit=False)

            # Excluir venda (sem auto_commit)
            db.excluir_venda(venda_id, auto_commit=False)

            db.commit()

            logger.info(f"Venda {venda_id} excluída via API - Estoque devolvido: {venda[2]}")
            return Mensagem(
                mensagem="Venda excluída com sucesso!",
                detalhes=f"Estoque devolvido: {venda[2]} unidades"
            )
        except Exception:
            db.rollback()
            raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir venda: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir venda: {str(e)}")
