"""
Sistema CRUD - Loja
Projeto refatorado com:
- Prepared statements (segurança contra SQL Injection)
- Variáveis de ambiente (.env)
- Tratamento de erros completo
- Validações de entrada
- Código modular e reutilizável
- Logging e transações
- Busca/filtro e relatórios
- API REST com FastAPI
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from database import DatabaseManager
from validators import (
    validar_inteiro_positivo,
    validar_float_positivo,
    validar_string_nao_vazia,
    validar_data,
    validar_preco
)
from utils import limpar_tela, formatar_moeda

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class SistemaLoja:
    def __init__(self, db_manager=None):
        """Inicializa o sistema com conexão ao banco de dados."""
        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_DATABASE", "loja")
        }
        self.db = db_manager if db_manager else DatabaseManager(config)
        logger.info("Sistema iniciado com sucesso")

    def exibir_produtos(self, produtos=None):
        """Exibe lista de produtos formatada."""
        if produtos is None:
            produtos = self.db.buscar_todos_produtos()

        if not produtos:
            print("\nNenhum produto encontrado!")
            return

        print("\n" + "="*60)
        print("LISTA DE PRODUTOS".center(60))
        print("="*60)
        for produto in produtos:
            print(f"""
ID: {produto[0]}
Nome: {produto[1]}
Descrição: {produto[2]}
Quantidade disponível: {produto[3]}
Preço: {formatar_moeda(produto[4])}
""")
            print("-"*60)

    def exibir_vendas(self, vendas=None):
        """Exibe lista de vendas formatada."""
        if vendas is None:
            vendas = self.db.buscar_todas_vendas()

        if not vendas:
            print("\nNenhuma venda encontrada!")
            return

        print("\n" + "="*60)
        print("LISTA DE VENDAS".center(60))
        print("="*60)
        for venda in vendas:
            print(f"""
ID da Venda: {venda[0]}
Nome do Produto: {venda[1]}
Quantidade Vendida: {venda[2]}
Data da Venda: {venda[3]}
""")
            print("-"*60)

    def cadastrar_produto(self):
        """Cadastra um novo produto com validações."""
        print("\n--- CADASTRO DE PRODUTO ---")

        nome = validar_string_nao_vazia("Digite o nome do produto: ")
        descricao = validar_string_nao_vazia("Digite a descrição do produto: ")
        qntd_disponivel = validar_inteiro_positivo("Digite a quantidade disponível: ")
        preco = validar_preco("Digite o preço do produto: ")

        try:
            self.db.inserir_produto(nome, descricao, qntd_disponivel, preco)
            print(f"\n✅ Produto '{nome}' cadastrado com sucesso!")
            logger.info(f"Produto cadastrado: {nome}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar produto: {e}")
            logger.error(f"Erro ao cadastrar produto: {e}")

    def visualizar_produtos(self):
        """Visualiza todos os produtos."""
        self.exibir_produtos()

    def editar_produto(self):
        """Edita um produto existente."""
        print("\n--- EDIÇÃO DE PRODUTO ---")

        # Mostrar produtos disponíveis
        self.exibir_produtos()

        id_editado = validar_inteiro_positivo("Digite o ID do produto que deseja editar: ")

        # Verificar se produto existe
        produto = self.db.buscar_produto_por_id(id_editado)
        if not produto:
            print("❌ Produto não encontrado!")
            return

        print(f"\nProduto selecionado: {produto[1]}")

        while True:
            submenu = input("""
Escolha o que deseja editar:
1 - Alterar nome
2 - Alterar descrição
3 - Alterar quantidade disponível
4 - Alterar preço
0 - Voltar ao menu principal
>> """)

            match submenu:
                case "1":
                    novo_nome = validar_string_nao_vazia("Digite o novo nome: ")
                    self.db.atualizar_nome_produto(novo_nome, id_editado)
                    print("✅ Nome atualizado com sucesso!")
                    logger.info(f"Produto {id_editado} - nome atualizado")

                case "2":
                    nova_descricao = validar_string_nao_vazia("Digite a nova descrição: ")
                    self.db.atualizar_descricao_produto(nova_descricao, id_editado)
                    print("✅ Descrição atualizada com sucesso!")
                    logger.info(f"Produto {id_editado} - descrição atualizada")

                case "3":
                    nova_qntd = validar_inteiro_positivo("Digite a nova quantidade disponível: ")
                    self.db.atualizar_quantidade_produto(nova_qntd, id_editado)
                    print("✅ Quantidade atualizada com sucesso!")
                    logger.info(f"Produto {id_editado} - quantidade atualizada")

                case "4":
                    novo_preco = validar_preco("Digite o novo preço: ")
                    self.db.atualizar_preco_produto(novo_preco, id_editado)
                    print("✅ Preço atualizado com sucesso!")
                    logger.info(f"Produto {id_editado} - preço atualizado")

                case "0":
                    print("Voltando ao menu principal...")
                    break

                case _:
                    print("❌ Opção inválida! Tente novamente.")
                    continue

            # Perguntar se deseja continuar editando
            continuar = input("\nDeseja editar mais alguma coisa neste produto? (S/N): ").upper()
            if continuar != "S":
                break

    def excluir_produto(self):
        """Exclui um produto com confirma."""
        print("\n--- EXCLUSÃO DE PRODUTO ---")

        # Mostrar produtos disponíveis
        produtos = self.db.buscar_todos_produtos()
        if not produtos:
            print("Nenhum produto cadastrado!")
            return

        self.exibir_produtos(produtos)

        id_excluido = validar_inteiro_positivo("Digite o ID do produto que deseja excluir: ")

        # Verificar se produto existe
        produto = self.db.buscar_produto_por_id(id_excluido)
        if not produto:
            print("❌ Produto não encontrado!")
            return

        # Confirmação
        print(f"\nProduto selecionado: {produto[1]}")
        confirmacao = input("Tem certeza que deseja excluir este produto? (S/N): ").upper()

        if confirmacao == "S":
            try:
                self.db.excluir_produto(id_excluido)
                print("✅ Produto excluído com sucesso!")
                logger.info(f"Produto excluído: {produto[1]} (ID: {id_excluido})")
            except Exception as e:
                print(f"❌ Erro ao excluir produto: {e}")
                logger.error(f"Erro ao excluir produto {id_excluido}: {e}")
        else:
            print("Operação de exclusão cancelada.")

    def cadastrar_venda(self):
        """Cadastra uma nova venda com controle de estoque."""
        print("\n--- CADASTRO DE VENDA ---")

        # Mostrar produtos disponíveis
        produtos = self.db.buscar_todos_produtos()
        if not produtos:
            print("Nenhum produto cadastrado! Cadastre um produto primeiro.")
            return

        print("\nProdutos disponíveis:")
        for produto in produtos:
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Qtd: {produto[3]} | Preço: {formatar_moeda(produto[4])}")

        id_produto = validar_inteiro_positivo("\nDigite o ID do produto que deseja vender: ")

        # Verificar se produto existe
        produto = self.db.buscar_produto_por_id(id_produto)
        if not produto:
            print("❌ Produto não encontrado!")
            return

        qntd_disponivel = produto[3]
        if qntd_disponivel <= 0:
            print("❌ Produto sem estoque!")
            return

        qntd_vendida = validar_inteiro_positivo("Digite a quantidade vendida: ")

        if qntd_vendida > qntd_disponivel:
            print(f"❌ Quantidade vendida ({qntd_vendida}) excede a disponível ({qntd_disponivel})!")
            return

        data_venda = validar_data("Digite a data da venda (DD/MM/AAAA ou deixe vazio para hoje): ")

        try:
            # Usar transação para garantir consistência
            self.db.iniciar_transacao()
            try:
                # Registrar venda
                self.db.registrar_venda(id_produto, qntd_vendida, data_venda)

                # Atualizar estoque
                nova_qntd = qntd_disponivel - qntd_vendida
                self.db.atualizar_quantidade_produto(nova_qntd, id_produto)

                # Confirmar transação
                self.db.commit()

                print(f"\n✅ Venda registrada com sucesso!")
                print(f"Produto: {produto[1]}")
                print(f"Quantidade: {qntd_vendida}")
                print(f"Estoque restante: {nova_qntd}")
                logger.info(f"Venda registrada: {qntd_vendida}x {produto[1]}")

            except Exception:
                # Rollback em caso de erro
                self.db.rollback()
                raise

        except Exception as e:
            print(f"\n❌ Erro ao registrar venda: {e}")
            logger.error(f"Erro ao registrar venda: {e}")

    def visualizar_vendas(self):
        """Visualiza todas as vendas."""
        self.exibir_vendas()

    def editar_venda(self):
        """Edita uma venda existente."""
        print("\n--- EDIÇÃO DE VENDA ---")

        # Mostrar vendas disponíveis
        vendas = self.db.buscar_todas_vendas()
        if not vendas:
            print("Nenhuma venda registrada!")
            return

        self.exibir_vendas(vendas)

        id_venda = validar_inteiro_positivo("Digite o ID da venda que deseja editar: ")

        # Verificar se venda existe
        venda = self.db.buscar_venda_por_id(id_venda)
        if not venda:
            print("❌ Venda não encontrada!")
            return

        print(f"\nVenda selecionada: {venda[1]} - Qtd: {venda[2]} - Data: {venda[3]}")

        while True:
            submenu = input("""
Escolha o que deseja editar:
1 - Alterar quantidade vendida
2 - Alterar data da venda
0 - Voltar ao menu principal
>> """)

            match submenu:
                case "1":
                    # Obter produto e quantidade atual
                    produto_id = self.db.buscar_id_produto_da_venda(id_venda)
                    if not produto_id:
                        print("❌ Erro ao buscar dados da venda!")
                        break

                    produto = self.db.buscar_produto_por_id(produto_id)
                    qntd_atual = venda[2]
                    qntd_estoque_atual = produto[3]

                    # Calcular novo estoque disponível
                    estoque_real = qntd_estoque_atual + qntd_atual
                    print(f"\nEstoque atual do produto: {estoque_real}")

                    nova_qntd = validar_inteiro_positivo("Digite a nova quantidade vendida: ")

                    if nova_qntd > estoque_real:
                        print(f"❌ Quantidade excede o estoque disponível ({estoque_real})!")
                        continue

                    # Usar transação para garantir consistência
                    try:
                        self.db.iniciar_transacao()
                        try:
                            # Atualizar venda e estoque
                            novo_estoque = estoque_real - nova_qntd
                            self.db.atualizar_quantidade_venda(nova_qntd, id_venda)
                            self.db.atualizar_quantidade_produto(novo_estoque, produto_id)
                            self.db.commit()

                            print("✅ Quantidade atualizada com sucesso!")
                            logger.info(f"Venda {id_venda} - quantidade atualizada para {nova_qntd}")

                        except Exception:
                            self.db.rollback()
                            raise

                    except Exception as e:
                        print(f"❌ Erro ao atualizar quantidade: {e}")
                        logger.error(f"Erro ao atualizar venda {id_venda}: {e}")

                case "2":
                    nova_data = validar_data("Digite a nova data da venda (DD/MM/AAAA): ")
                    self.db.atualizar_data_venda(nova_data, id_venda)
                    print("✅ Data atualizada com sucesso!")
                    logger.info(f"Venda {id_venda} - data atualizada")

                case "0":
                    print("Voltando ao menu principal...")
                    break

                case _:
                    print("❌ Opção inválida! Tente novamente.")
                    continue

            continuar = input("\nDeseja editar mais alguma coisa nesta venda? (S/N): ").upper()
            if continuar != "S":
                break

    def excluir_venda(self):
        """Exclui uma venda com confirma e devolve estoque."""
        print("\n--- EXCLUSÃO DE VENDA ---")

        # Mostrar vendas disponíveis
        vendas = self.db.buscar_todas_vendas()
        if not vendas:
            print("Nenhuma venda registrada!")
            return

        self.exibir_vendas(vendas)

        id_venda = validar_inteiro_positivo("Digite o ID da venda que deseja excluir: ")

        # Verificar se venda existe
        venda = self.db.buscar_venda_por_id(id_venda)
        if not venda:
            print("❌ Venda não encontrada!")
            return

        print(f"\nVenda selecionada: {venda[1]} - Qtd: {venda[2]}")

        confirmacao = input("Tem certeza que deseja excluir esta venda? (S/N): ").upper()

        if confirmacao == "S":
            try:
                # Usar transação para garantir consistência
                self.db.iniciar_transacao()
                try:
                    # Obter dados da venda
                    produto_id = self.db.buscar_id_produto_da_venda(id_venda)
                    if not produto_id:
                        raise Exception("Produto da venda não encontrado")

                    produto = self.db.buscar_produto_por_id(produto_id)
                    novo_estoque = produto[3] + venda[2]

                    # Devolver produto ao estoque
                    self.db.atualizar_quantidade_produto(novo_estoque, produto_id)

                    # Excluir venda
                    self.db.excluir_venda(id_venda)

                    # Confirmar transação
                    self.db.commit()

                    print("✅ Venda excluída com sucesso!")
                    print(f"Estoque devolvido: {venda[2]} unidades")
                    logger.info(f"Venda excluída: {id_venda} - Estoque devolvido: {venda[2]}")

                except Exception:
                    self.db.rollback()
                    raise

            except Exception as e:
                print(f"❌ Erro ao excluir venda: {e}")
                logger.error(f"Erro ao excluir venda {id_venda}: {e}")
        else:
            print("Operação de exclusão cancelada.")

    def buscar_produto(self):
        """Busca produto por nome, ID ou faixa de preço."""
        print("\n--- BUSCA DE PRODUTO ---")

        tipo_busca = input("""
Escolha o tipo de busca:
1 - Buscar por ID
2 - Buscar por nome
3 - Buscar por faixa de preço
>> """)

        match tipo_busca:
            case "1":
                id_produto = validar_inteiro_positivo("Digite o ID do produto: ")
                produto = self.db.buscar_produto_por_id(id_produto)
                if produto:
                    self.exibir_produtos([produto])
                else:
                    print("❌ Produto não encontrado!")

            case "2":
                nome = input("Digite o nome ou parte do nome: ").strip()
                if not nome:
                    print("❌ Digite um nome válido!")
                    return
                produtos = self.db.buscar_produto_por_nome(nome)
                if produtos:
                    self.exibir_produtos(produtos)
                else:
                    print("❌ Nenhum produto encontrado!")

            case "3":
                preco_min = validar_preco("Digite o preço mínimo: ")
                preco_max = validar_preco("Digite o preço máximo: ")

                if preco_min > preco_max:
                    print("❌ Preço mínimo deve ser menor que o máximo!")
                    return

                produtos = self.db.buscar_produto_por_faixa_preco(preco_min, preco_max)
                if produtos:
                    self.exibir_produtos(produtos)
                else:
                    print("❌ Nenhum produto encontrado nesta faixa!")

            case _:
                print("❌ Opção inválida!")

    def relatorio_vendas(self):
        """Gera relatório de vendas por período."""
        print("\n--- RELATÓRIO DE VENDAS ---")

        print("Digite o período desejado:")
        data_inicio = validar_data("Data inicial (DD/MM/AAAA ou vazio para início): ")
        data_fim = validar_data("Data final (DD/MM/AAAA ou vazio para hoje): ")

        if not data_inicio:
            data_inicio = "2000-01-01"
        if not data_fim:
            data_fim = datetime.now().strftime("%Y-%m-%d")

        vendas = self.db.buscar_vendas_por_periodo(data_inicio, data_fim)

        if not vendas:
            print("\nNenhuma venda encontrada neste período!")
            return

        self.exibir_vendas(vendas)

        # Resumo
        total_vendas = len(vendas)
        total_itens = sum(venda[2] for venda in vendas)

        print("\n" + "="*60)
        print("RESUMO DO PERÍODO".center(60))
        print("="*60)
        print(f"Total de vendas: {total_vendas}")
        print(f"Total de itens vendidos: {total_itens}")
        print("="*60)

    def menu_principal(self):
        """Exibe o menu principal e gerencia as opções."""
        while True:
            limpar_tela()
            print("\n" + "="*40)
            print("SISTEMA CRUD - LOJA".center(40))
            print("="*40)
            print("""
Escolha uma opção:

--- PRODUTOS ---
1 - Cadastrar novo produto
2 - Ver todos os produtos
3 - Buscar produto
4 - Editar um produto
5 - Excluir um produto

--- VENDAS ---
6 - Cadastrar venda
7 - Ver todas as vendas
8 - Relatório de vendas por período
9 - Editar uma venda
10 - Excluir uma venda

0 - Sair
""")

            opcao = input(">> ").strip()

            match opcao:
                case "1":
                    self.cadastrar_produto()
                case "2":
                    self.visualizar_produtos()
                case "3":
                    self.buscar_produto()
                case "4":
                    self.editar_produto()
                case "5":
                    self.excluir_produto()
                case "6":
                    self.cadastrar_venda()
                case "7":
                    self.visualizar_vendas()
                case "8":
                    self.relatorio_vendas()
                case "9":
                    self.editar_venda()
                case "10":
                    self.excluir_venda()
                case "0":
                    print("\nSaindo do sistema...")
                    logger.info("Sistema encerrado")
                    self.db.fechar_conexao()
                    break
                case _:
                    print("\n❌ Opção inválida! Tente novamente.")

            input("\nPressione ENTER para continuar...")


# ==================== FASTAPI APP ====================

def criar_app_api():
    """
    Cria e configura a aplicação FastAPI.
    Esta função é usada quando o servidor API é iniciado.
    """
    from fastapi import FastAPI
    from api import configure_api_routes
    
    app = FastAPI(
        title="🏪 Gestão Loja API",
        description="""
        API REST para sistema de gerenciamento de produtos e vendas.
        
        ## Funcionalidades
        
        * **Produtos** - CRUD completo com busca avançada por nome e faixa de preço
        * **Vendas** - Registro com controle automático de estoque
        * **Relatórios** - Relatório de vendas por período com resumo
        
        ## Segurança
        
        * Prepared statements contra SQL Injection
        * Transações atômicas para consistência de dados
        * Validações robustas em todas as entradas
        """,
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Inicializar banco de dados e compartilhar com o app
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_DATABASE", "loja")
    }
    db = DatabaseManager(config)
    app.state.db = db
    
    # Configurar rotas
    configure_api_routes(app)
    
    # Eventos de startup e shutdown
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 API Gestão Loja iniciada")
        print("✅ API rodando! Acesse:")
        print("   📖 Documentação Swagger: http://localhost:8000/docs")
        print("   📘 Documentação ReDoc: http://localhost:8000/redoc")
        print("   🔌 Health Check: http://localhost:8000/health")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("🛑 API Gestão Loja encerrada")
        db.fechar_conexao()
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Endpoint para verificar status da API."""
        return {"status": "ok", "servico": "Gestão Loja API", "versao": "2.0.0"}
    
    return app


# Criar instância do app para uvicorn
app = criar_app_api()


def main():
    """Função principal para modo CLI."""
    try:
        sistema = SistemaLoja()
        sistema.menu_principal()
    except Exception as e:
        logger.critical(f"Erro crítico no sistema: {e}")
        print(f"\n❌ Erro crítico: {e}")
        print("Verifique o arquivo sistema.log para mais detalhes.")


if __name__ == "__main__":
    # Verificar se deve iniciar em modo API ou CLI
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        # Modo API
        import uvicorn
        print("🚀 Iniciando API REST...")
        uvicorn.run(
            "main:app",
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            reload=True
        )
    else:
        # Modo CLI (padrão)
        main()
