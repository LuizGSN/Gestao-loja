"""
Schemas Pydantic para validação e documentação da API.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


# ==================== PRODUTO ====================

class ProdutoBase(BaseModel):
    """Schema base para produto."""
    nome: str = Field(..., min_length=1, max_length=60, description="Nome do produto")
    descricao: str = Field(..., min_length=1, max_length=150, description="Descrição do produto")
    qntd_disponivel: int = Field(..., ge=0, description="Quantidade disponível em estoque")
    preco: float = Field(..., ge=0, le=999999999, description="Preço do produto")


class ProdutoCreate(ProdutoBase):
    """Schema para criar produto."""
    pass


class ProdutoUpdate(BaseModel):
    """Schema para atualizar produto (todos os campos opcionais)."""
    nome: Optional[str] = Field(None, min_length=1, max_length=60)
    descricao: Optional[str] = Field(None, min_length=1, max_length=150)
    qntd_disponivel: Optional[int] = Field(None, ge=0)
    preco: Optional[float] = Field(None, ge=0, le=999999999)


class ProdutoResponse(ProdutoBase):
    """Schema de resposta de produto."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==================== VENDA ====================

class VendaBase(BaseModel):
    """Schema base para venda."""
    id_produto: int = Field(..., gt=0, description="ID do produto vendido")
    qntd_vendida: int = Field(..., gt=0, description="Quantidade vendida")
    data_venda: date = Field(..., description="Data da venda")


class VendaCreate(BaseModel):
    """Schema para criar venda."""
    id_produto: int = Field(..., gt=0, description="ID do produto vendido")
    qntd_vendida: int = Field(..., gt=0, description="Quantidade vendida")
    data_venda: Optional[date] = Field(None, description="Data da venda (opcional, usa data atual)")


class VendaUpdate(BaseModel):
    """Schema para atualizar venda."""
    qntd_vendida: Optional[int] = Field(None, gt=0)
    data_venda: Optional[date] = None


class VendaResponse(BaseModel):
    """Schema de resposta de venda."""
    id: int
    produto_nome: str
    qntd_vendida: int
    data_venda: date

    model_config = ConfigDict(from_attributes=True)


# ==================== RELATÓRIOS ====================

class RelatorioVendas(BaseModel):
    """Schema para relatório de vendas."""
    data_inicio: Optional[date] = Field(None, description="Data inicial do filtro")
    data_fim: Optional[date] = Field(None, description="Data final do filtro")


class ResumoVendas(BaseModel):
    """Schema de resumo de vendas."""
    total_vendas: int
    total_itens_vendidos: int
    vendas: list[VendaResponse]


# ==================== BUSCA ====================

class BuscaProduto(BaseModel):
    """Schema para busca de produtos."""
    tipo_busca: str = Field(..., description="Tipo de busca: 'id', 'nome' ou 'faixa_preco'")
    id_produto: Optional[int] = Field(None, gt=0, description="ID do produto (para busca por ID)")
    nome: Optional[str] = Field(None, min_length=1, description="Nome ou parte do nome (para busca por nome)")
    preco_min: Optional[float] = Field(None, ge=0, description="Preço mínimo (para busca por faixa)")
    preco_max: Optional[float] = Field(None, ge=0, description="Preço máximo (para busca por faixa)")


# ==================== MENSAGENS ====================

class Mensagem(BaseModel):
    """Schema para mensagens de resposta."""
    mensagem: str
    detalhes: Optional[str] = None
