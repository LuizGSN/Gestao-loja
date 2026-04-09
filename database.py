"""
Módulo de gerenciamento do banco de dados.
Usa prepared statements para prevenir SQL Injection.
"""

import mysql.connector
import logging
from mysql.connector import Error

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gerencia conexões e operações no banco de dados."""
    
    def __init__(self, config):
        """Inicializa com configurações do banco."""
        self.config = config
        self.conexao = None
        logger.info("DatabaseManager inicializado")
    
    def conectar(self):
        """Estabelece conexão com o banco de dados."""
        try:
            self.conexao = mysql.connector.connect(**self.config)
            if self.conexao.is_connected():
                logger.info("Conexão com banco de dados estabelecida")
        except Error as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            logger.info("Conexão com banco de dados fechada")

    def iniciar_transacao(self):
        """Inicia uma nova transação."""
        self._garantir_conexao()
        self.conexao.start_transaction()
        logger.debug("Transação iniciada")

    def commit(self):
        """Confirma a transação atual."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.commit()
            logger.debug("Transação confirmada (commit)")

    def rollback(self):
        """Reverte a transação atual."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.rollback()
            logger.warning("Transação revertida (rollback)")
    
    def _garantir_conexao(self):
        """Garante que existe uma conexão ativa."""
        if not self.conexao or not self.conexao.is_connected():
            self.conectar()
    
    def executar_atualizacao(self, query, params=None):
        """
        Executa comando de atualização (INSERT, UPDATE, DELETE) com prepared statement.
        
        Args:
            query: SQL query com placeholders (%s)
            params: Parâmetros para substituir nos placeholders
        """
        try:
            self._garantir_conexao()
            cursor = self.conexao.cursor()
            cursor.execute(query, params)
            self.conexao.commit()
            cursor.close()
            logger.debug(f"Query executada com sucesso: {query[:50]}...")
        except Error as e:
            logger.error(f"Erro na execução da query: {e}\nQuery: {query}")
            if self.conexao:
                self.conexao.rollback()
            raise
    
    def executar_busca(self, query, params=None):
        """
        Executa comando de busca (SELECT) com prepared statement.
        
        Args:
            query: SQL query com placeholders (%s)
            params: Parâmetros para substituir nos placeholders
            
        Returns:
            Lista de resultados
        """
        try:
            self._garantir_conexao()
            cursor = self.conexao.cursor()
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Error as e:
            logger.error(f"Erro na execução da busca: {e}\nQuery: {query}")
            raise
    
    # ==========================================
    # OPERAÇÕES DE PRODUTO
    # ==========================================
    
    def inserir_produto(self, nome, descricao, qntd_disponivel, preco):
        """Insere um novo produto usando prepared statement."""
        query = """
            INSERT INTO produto (nome, descricao, qntd_disponivel, preco) 
            VALUES (%s, %s, %s, %s)
        """
        params = (nome, descricao, qntd_disponivel, preco)
        self.executar_atualizacao(query, params)
    
    def buscar_todos_produtos(self):
        """Busca todos os produtos."""
        query = "SELECT * FROM produto ORDER BY id"
        return self.executar_busca(query)
    
    def buscar_produto_por_id(self, id_produto):
        """Busca produto por ID."""
        query = "SELECT * FROM produto WHERE id = %s"
        params = (id_produto,)
        resultados = self.executar_busca(query, params)
        return resultados[0] if resultados else None
    
    def buscar_produto_por_nome(self, nome):
        """Busca produto por nome (busca parcial)."""
        query = "SELECT * FROM produto WHERE nome LIKE %s ORDER BY id"
        params = (f"%{nome}%",)
        return self.executar_busca(query, params)
    
    def buscar_produto_por_faixa_preco(self, preco_min, preco_max):
        """Busca produto por faixa de preço."""
        query = "SELECT * FROM produto WHERE preco BETWEEN %s AND %s ORDER BY preco"
        params = (preco_min, preco_max)
        return self.executar_busca(query, params)
    
    def atualizar_nome_produto(self, nome, id_produto):
        """Atualiza nome do produto."""
        query = "UPDATE produto SET nome = %s WHERE id = %s"
        params = (nome, id_produto)
        self.executar_atualizacao(query, params)
    
    def atualizar_descricao_produto(self, descricao, id_produto):
        """Atualiza descrição do produto."""
        query = "UPDATE produto SET descricao = %s WHERE id = %s"
        params = (descricao, id_produto)
        self.executar_atualizacao(query, params)
    
    def atualizar_quantidade_produto(self, qntd_disponivel, id_produto):
        """Atualiza quantidade disponível do produto."""
        query = "UPDATE produto SET qntd_disponivel = %s WHERE id = %s"
        params = (qntd_disponivel, id_produto)
        self.executar_atualizacao(query, params)
    
    def atualizar_preco_produto(self, preco, id_produto):
        """Atualiza preço do produto."""
        query = "UPDATE produto SET preco = %s WHERE id = %s"
        params = (preco, id_produto)
        self.executar_atualizacao(query, params)
    
    def excluir_produto(self, id_produto):
        """Exclui um produto."""
        query = "DELETE FROM produto WHERE id = %s"
        params = (id_produto,)
        self.executar_atualizacao(query, params)
    
    # ==========================================
    # OPERAÇÕES DE VENDA
    # ==========================================
    
    def buscar_todas_vendas(self):
        """Busca todas as vendas com join para produto."""
        query = """
            SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
            FROM venda
            JOIN produto ON venda.id_produto = produto.id
            ORDER BY venda.id DESC
        """
        return self.executar_busca(query)
    
    def buscar_venda_por_id(self, id_venda):
        """Busca venda por ID."""
        query = """
            SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
            FROM venda
            JOIN produto ON venda.id_produto = produto.id
            WHERE venda.id = %s
        """
        params = (id_venda,)
        resultados = self.executar_busca(query, params)
        return resultados[0] if resultados else None
    
    def buscar_id_produto_da_venda(self, id_venda):
        """Busca ID do produto associado a uma venda."""
        query = "SELECT id_produto FROM venda WHERE id = %s"
        params = (id_venda,)
        resultados = self.executar_busca(query, params)
        return resultados[0][0] if resultados else None
    
    def buscar_vendas_por_periodo(self, data_inicio, data_fim):
        """Busca vendas por período."""
        query = """
            SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
            FROM venda
            JOIN produto ON venda.id_produto = produto.id
            WHERE venda.data_venda BETWEEN %s AND %s
            ORDER BY venda.data_venda DESC
        """
        params = (data_inicio, data_fim)
        return self.executar_busca(query, params)
    
    def registrar_venda(self, id_produto, qntd_vendida, data_venda):
        """Registra uma nova venda."""
        query = """
            INSERT INTO venda (id_produto, qntd_vendida, data_venda) 
            VALUES (%s, %s, %s)
        """
        params = (id_produto, qntd_vendida, data_venda)
        self.executar_atualizacao(query, params)
    
    def atualizar_quantidade_venda(self, qntd_vendida, id_venda):
        """Atualiza quantidade vendida."""
        query = "UPDATE venda SET qntd_vendida = %s WHERE id = %s"
        params = (qntd_vendida, id_venda)
        self.executar_atualizacao(query, params)
    
    def atualizar_data_venda(self, data_venda, id_venda):
        """Atualiza data da venda."""
        query = "UPDATE venda SET data_venda = %s WHERE id = %s"
        params = (data_venda, id_venda)
        self.executar_atualizacao(query, params)
    
    def excluir_venda(self, id_venda):
        """Exclui uma venda."""
        query = "DELETE FROM venda WHERE id = %s"
        params = (id_venda,)
        self.executar_atualizacao(query, params)
