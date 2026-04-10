"""
Testes de integração para a API REST.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import Mock, patch
from datetime import date

from main import criar_app_api


@pytest.fixture
def app():
    """Cria a aplicação FastAPI para testes."""
    return criar_app_api()


@pytest.fixture
def mock_db():
    """Cria um mock do DatabaseManager."""
    db = Mock()
    
    # Configurar métodos mock
    db.buscar_todos_produtos.return_value = [
        (1, "Notebook", "Notebook gamer", 10, 4500.00),
        (2, "Mouse", "Mouse sem fio", 50, 89.90)
    ]
    
    db.buscar_produto_por_id.return_value = (1, "Notebook", "Notebook gamer", 10, 4500.00)
    db.buscar_produto_por_nome.return_value = [(1, "Notebook", "Notebook gamer", 10, 4500.00)]
    db.buscar_produto_por_faixa_preco.return_value = [
        (2, "Mouse", "Mouse sem fio", 50, 89.90)
    ]
    
    db.buscar_todas_vendas.return_value = [
        (1, "Notebook", 2, date(2024, 1, 15)),
        (2, "Mouse", 5, date(2024, 1, 16))
    ]
    
    db.buscar_venda_por_id.return_value = (1, "Notebook", 2, date(2024, 1, 15))
    db.buscar_id_produto_da_venda.return_value = 1
    
    db.buscar_vendas_por_periodo.return_value = [
        (1, "Notebook", 2, date(2024, 1, 15))
    ]
    
    return db


@pytest.fixture
async def client(app, mock_db):
    """Cria um cliente de teste HTTP."""
    # Injetar mock db no app
    app.state.db = mock_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ==================== TESTES DE PRODUTOS ====================

class TestProdutosAPI:
    
    @pytest.mark.asyncio
    async def test_listar_produtos(self, client, mock_db):
        """Testa listagem de produtos."""
        async with client as c:
            response = await c.get("/api/v1/produtos/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["nome"] == "Notebook"
        assert data[0]["preco"] == 4500.00
    
    @pytest.mark.asyncio
    async def test_buscar_produto_por_id(self, client, mock_db):
        """Testa busca de produto por ID."""
        async with client as c:
            response = await c.get("/api/v1/produtos/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["nome"] == "Notebook"
    
    @pytest.mark.asyncio
    async def test_buscar_produto_nao_encontrado(self, client, mock_db):
        """Testa busca de produto inexistente."""
        mock_db.buscar_produto_por_id.return_value = None
        
        async with client as c:
            response = await c.get("/api/v1/produtos/999")
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_criar_produto(self, client, mock_db):
        """Testa criação de produto."""
        mock_db.inserir_produto.return_value = None
        
        produto_data = {
            "nome": "Teclado",
            "descricao": "Teclado mecânico",
            "qntd_disponivel": 30,
            "preco": 299.90
        }
        
        async with client as c:
            response = await c.post("/api/v1/produtos/", json=produto_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "sucesso" in data["mensagem"].lower()
    
    @pytest.mark.asyncio
    async def test_atualizar_produto(self, client, mock_db):
        """Testa atualização de produto."""
        mock_db.atualizar_nome_produto.return_value = None
        
        update_data = {"nome": "Notebook Pro"}
        
        async with client as c:
            response = await c.put("/api/v1/produtos/1", json=update_data)
        
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_excluir_produto(self, client, mock_db):
        """Testa exclusão de produto."""
        mock_db.excluir_produto.return_value = None
        
        async with client as c:
            response = await c.delete("/api/v1/produtos/1")
        
        assert response.status_code == 200


# ==================== TESTES DE VENDAS ====================

class TestVendasAPI:
    
    @pytest.mark.asyncio
    async def test_listar_vendas(self, client, mock_db):
        """Testa listagem de vendas."""
        async with client as c:
            response = await c.get("/api/v1/vendas/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    @pytest.mark.asyncio
    async def test_criar_venda(self, client, mock_db):
        """Testa criação de venda."""
        mock_db.registrar_venda.return_value = None
        mock_db.atualizar_quantidade_produto.return_value = None
        mock_db.iniciar_transacao.return_value = None
        mock_db.commit.return_value = None
        
        venda_data = {
            "id_produto": 1,
            "qntd_vendida": 2,
            "data_venda": "2024-01-20"
        }
        
        async with client as c:
            response = await c.post("/api/v1/vendas/", json=venda_data)
        
        assert response.status_code == 201
    
    @pytest.mark.asyncio
    async def test_criar_venda_sem_estoque(self, client, mock_db):
        """Testa criação de venda com estoque insuficiente."""
        mock_db.buscar_produto_por_id.return_value = (1, "Notebook", "Notebook", 1, 4500.00)
        
        venda_data = {
            "id_produto": 1,
            "qntd_vendida": 5,  # Mais do que estoque
            "data_venda": "2024-01-20"
        }
        
        async with client as c:
            response = await c.post("/api/v1/vendas/", json=venda_data)
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_relatorio_vendas(self, client, mock_db):
        """Testa relatório de vendas."""
        async with client as c:
            response = await c.get("/api/v1/vendas/relatorio/periodo?data_inicio=2024-01-01&data_fim=2024-01-31")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas" in data
        assert "vendas" in data


# ==================== TESTES DE HEALTH CHECK ====================

class TestHealthCheck:
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Testa endpoint de health check."""
        async with client as c:
            response = await c.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "API" in data["servico"]
