# GESTAO-LOJA

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)

> Sistema de gerenciamento de produtos e vendas com banco de dados MySQL e back-end em Python.

## ✨ FUNCIONALIDADES

* CRUD completo — criar, listar, buscar, editar e excluir produtos
* CRUD completo de vendas — registro com controle automático de estoque
* Busca avançada — por ID, nome ou faixa de preço
* Relatório de vendas — filtro por período com resumo de itens e total
* Validações robustas — inteiros, floats, datas e strings validados antes de processar
* Logging automático — auditoria completa em `sistema.log`
* Transações atômicas — commit/rollback para consistência dos dados
* Prepared statements — proteção contra SQL Injection

## 🛠️ TECNOLOGIAS

| Backend | Banco de Dados | Configuração |
|---------|---------------|--------------|
| ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python) | ![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?logo=mysql) | ![dotenv](https://img.shields.io/badge/python--dotenv-black?logo=python) |
| POO | Transações ACID | .env |
| Prepared statements | Prepared statements | |

## 📋 PRÉ-REQUISITOS

* Python 3.10 ou superior
* MySQL Server >= 8.0
* pip

## 🚀 INSTALAÇÃO

### 1. CLONE O REPOSITÓRIO
```bash
git clone https://github.com/LuizGSN/Gestao-loja.git
cd Gestao-loja
```

### 2. INSTALE AS DEPENDÊNCIAS
```bash
pip install -r requirements.txt
```

### 3. CRIE O BANCO DE DADOS
```bash
mysql -u root -p < projeto_crud.sql
```
Ou execute manualmente:
```sql
CREATE DATABASE loja;
USE loja;
-- O script completo está em projeto_crud.sql
```

### 4. CONFIGURE AS VARIÁVEIS DE AMBIENTE
```bash
copy .env.example .env
```
Edite o `.env` com suas credenciais:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_DATABASE=loja
```

### 5. EXECUTE A APLICAÇÃO
```bash
python main.py
```
O menu interativo aparecerá no terminal com opções para gerenciar produtos e vendas.

## 📁 ESTRUTURA DO PROJETO
```text
Gestao-loja/
├── main.py              # Programa principal com menu e lógica
├── database.py          # DatabaseManager — conexão e operações MySQL
├── validators.py        # Validações de entrada do usuário
├── utils.py             # Funções utilitárias (formatação, limpeza)
├── projeto_crud.sql     # Script de criação do banco
├── requirements.txt     # Dependências Python
├── .env.example         # Variáveis de ambiente modelo
├── .gitignore
└── README.md
```

## 🔒 SEGURANÇA

* Prepared statements com placeholders (`%s`) em todas as queries — proteção total contra SQL Injection
* Credenciais em arquivo `.env` (não versionado pelo `.gitignore`)
* Validação de entrada em todos os inputs — inteiros positivos, floats, datas e strings
* Transações atômicas com commit/rollback — consistência garantida em vendas e exclusões
* Logging de todas as operações — auditoria completa em `sistema.log`

## 🎯 BOAS PRÁTICAS

* POO — classes `SistemaLoja` e `DatabaseManager` com responsabilidades bem definidas
* DRY — código reutilizável com métodos específicos por operação
* Separação de responsabilidades — módulos lógicos separados (db, validação, utils, lógica)
* Tratamento de erros — try/except em todas as operações críticas
* Type hints — documentação de tipos em funções críticas

---

## 📝 LICENÇA

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

---

*Desenvolvido por Luiz Gonzaga — Estudante de Análise e Desenvolvimento de Sistemas*
