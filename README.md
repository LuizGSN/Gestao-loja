# 🛒 Gestao-loja

> Sistema de gerenciamento de produtos e vendas com banco de dados MySQL e back-end em Python.

----------------------------------------

## ✨ FUNCIONALIDADES

- **CRUD Completo** de produtos (criar, listar, buscar, editar, excluir)
- **CRUD Completo** de vendas com controle automático de estoque
- **Busca avançada** por ID, nome ou faixa de preço
- **Relatório de vendas** por período com resumo
- **Validações robustas** em todas as entradas do usuário
- **Logging automático** de todas as operações
- **Transações atômicas** para consistência dos dados
- **Prepared statements** para proteção contra SQL Injection

----------------------------------------

## 🛠️ STACK TECNOLÓGICA

| Categoria | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.10+ |
| Banco de Dados | MySQL 8.0+ |
| ORM/Driver | mysql-connector-python |
| Configuração | python-dotenv |
| Paradigma | Programação Orientada a Objetos |

----------------------------------------

## 📋 PRÉ-REQUISITOS

- Python 3.10 ou superior
- MySQL Server instalado e rodando
- Pip (gerenciador de pacotes Python)

----------------------------------------

## � COMO RODAR LOCALMENTE

### 1. Clone o repositório

```bash
git clone https://github.com/LuizGSN/Projeto_CRUD.git
cd Projeto_CRUD
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Crie o banco de dados

```bash
mysql -u root -p < projeto_crud.sql
```

Ou execute manualmente:

```bash
mysql -u root -p
```

```sql
create database loja;
use loja;
-- O script completo está em projeto_crud.sql
```

### 4. Configure as variáveis de ambiente

```bash
copy .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_DATABASE=loja
```

### 5. Execute a aplicação

```bash
python main.py
```

----------------------------------------

## 📁 ESTRUTURA DO PROJETO

```
Projeto_CRUD/
├── main.py              # Programa principal com menu e lógica
├── database.py          # Gerenciamento do banco de dados (DatabaseManager)
├── validators.py        # Validações de entrada do usuário
├── utils.py             # Funções utilitárias
├── projeto_crud.sql     # Script de criação do banco
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de configuração do banco
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Documentação do projeto
```

----------------------------------------

## 🔒 SEGURANÇA

- **SQL Injection**: Todas as queries usam prepared statements com placeholders (`%s`)
- **Credenciais protegidas**: Dados sensíveis em arquivo `.env` (não versionado)
- **Validações de entrada**: Inteiros positivos, floats, datas e strings validados antes de processar
- **Transações atômicas**: Operações de venda usam commit/rollback para garantir consistência

----------------------------------------

## 🎯 BOAS PRÁTICAS APLICADAS

- **POO**: Classes `SistemaLoja` e `DatabaseManager` com responsabilidades bem definidas
- **DRY**: Código reutilizável com métodos específicos para cada operação
- **Logging**: Auditoria completa com `sistema.log`
- **Tratamento de erros**: Try/except em todas as operações críticas
- **Separação de responsabilidades**: Código dividido em módulos lógicos
- **Type hints**: Documentação de tipos em funções críticas

----------------------------------------

## � LICENÇA

Este projeto é open-source e está disponível para uso educacional.

----------------------------------------

**⭐ Se este projeto te ajudou, deixe uma estrela!**
