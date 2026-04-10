# 🏪 GESTAO-LOJA

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Tests](https://github.com/LuizGSN/Gestao-loja/actions/workflows/ci-cd.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-70%25-yellowgreen)
![License](https://img.shields.io/badge/License-MIT-green)

> Sistema completo de gerenciamento de produtos e vendas com **API REST** e **CLI**, banco MySQL, testes automatizados e deploy com Docker.

---

## ✨ FUNCIONALIDADES

### 📦 Produtos
- ✅ CRUD completo via API e CLI
- ✅ Busca por ID, nome ou faixa de preço
- ✅ Validações robustas de entrada
- ✅ Controle de estoque integrado

### 💰 Vendas
- ✅ Registro com controle automático de estoque
- ✅ Edição de quantidade e data
- ✅ Exclusão com devolução automática de estoque
- ✅ Transações atômicas para consistência

### 📊 Relatórios
- ✅ Relatório de vendas por período
- ✅ Resumo com total de vendas e itens vendidos
- ✅ Filtro por data inicial e final

### 🔒 Segurança & Qualidade
- ✅ Prepared statements (SQL Injection protection)
- ✅ Logging completo de auditoria
- ✅ Testes unitários e de integração
- ✅ CI/CD pipeline com GitHub Actions
- ✅ Docker para fácil execução

---

## 🛠️ TECNOLOGIAS

| Backend | API | Banco de Dados | DevOps |
|---------|-----|----------------|--------|
| ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python) | ![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?logo=fastapi) | ![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?logo=mysql) | ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker) |
| POO | Swagger/OpenAPI | Transações ACID | GitHub Actions |
| Pydantic | Validações automáticas | Prepared Statements | pytest + coverage |
| Logging | Documentação automática | Foreign Keys | CI/CD Pipeline |

---

## 📋 PRÉ-REQUISITOS

**Para rodar localmente:**
- Python 3.10+
- MySQL Server 8.0+
- pip

**Para rodar com Docker:**
- Docker
- Docker Compose

---

## 🚀 INSTALAÇÃO & EXECUÇÃO

### 🎯 OPÇÃO 1: Execução Local (CLI)

#### 1. CLONE O REPOSITÓRIO
```bash
git clone https://github.com/LuizGSN/Gestao-loja.git
cd Gestao-loja
```

#### 2. INSTALE AS DEPENDÊNCIAS
```bash
pip install -r requirements.txt
```

#### 3. CRIE O BANCO DE DADOS
```bash
mysql -u root -p < projeto_crud.sql
```

Ou execute manualmente:
```sql
CREATE DATABASE loja;
USE loja;
-- O script completo está em projeto_crud.sql
```

#### 4. CONFIGURE AS VARIÁVEIS DE AMBIENTE
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o `.env` com suas credenciais:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_DATABASE=loja
```

#### 5. EXECUTE O SISTEMA (MODO CLI)
```bash
python main.py
```

---

### 🌐 OPÇÃO 2: API REST (Recomendado)

Após configurar o banco de dados (passos 1-4 acima):

```bash
python main.py --api
```

A API estará disponível em:
- **📖 Swagger UI:** http://localhost:8000/docs
- **📘 ReDoc:** http://localhost:8000/redoc
- **🔌 Health Check:** http://localhost:8000/health

**Exemplo de uso da API:**

```bash
# Listar produtos
curl http://localhost:8000/api/v1/produtos/

# Criar produto
curl -X POST http://localhost:8000/api/v1/produtos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Notebook Gamer",
    "descricao": "RTX 4060, 16GB RAM",
    "qntd_disponivel": 10,
    "preco": 4500.00
  }'

# Registrar venda
curl -X POST http://localhost:8000/api/v1/vendas/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_produto": 1,
    "qntd_vendida": 2,
    "data_venda": "2024-04-09"
  }'
```

---

### 🐳 OPÇÃO 3: Docker (Mais fácil)

#### 1. CLONE O REPOSITÓRIO
```bash
git clone https://github.com/LuizGSN/Gestao-loja.git
cd Gestao-loja
```

#### 2. SUBA OS CONTAINERS
```bash
docker-compose up -d
```

Isso irá:
- ✅ Criar container MySQL com banco configurada
- ✅ Criar container da API REST
- ✅ Criar container phpMyAdmin (opcional)

#### 3. ACESSE OS SERVIÇOS
- **🌐 API REST:** http://localhost:8000/docs
- **📊 phpMyAdmin:** http://localhost:8080
  - Usuário: `root`
  - Senha: `rootpassword`

#### 4. PARE OS CONTAINERS
```bash
docker-compose down
```

---

## 📁 ESTRUTURA DO PROJETO

```
Gestao-loja/
├── main.py                    # Programa principal (CLI + API)
├── database.py                # DatabaseManager — conexão e operações MySQL
├── validators.py              # Validações de entrada do usuário
├── utils.py                   # Funções utilitárias
├── projeto_crud.sql           # Script de criação do banco
├── requirements.txt           # Dependências Python
├── pyproject.toml             # Configurações pytest e coverage
├── pytest.ini                 # Configuração pytest
├── Dockerfile                 # Imagem Docker da API
├── docker-compose.yml         # Orquestração de containers
├── .env.example               # Variáveis de ambiente modelo
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD
├── api/
│   ├── __init__.py            # Configuração de rotas da API
│   ├── schemas.py             # Schemas Pydantic
│   └── routes/
│       ├── __init__.py
│       ├── produtos.py        # Endpoints de produtos
│       └── vendas.py          # Endpoints de vendas
├── tests/
│   ├── __init__.py
│   ├── test_utils.py          # Testes de utils
│   ├── test_validators.py     # Testes de validators
│   └── test_api.py            # Testes da API
└── README.md
```

---

## 🔒 SEGURANÇA

- ✅ **Prepared statements** com placeholders (`%s`) em todas as queries
- ✅ **Credenciais** em arquivo `.env` (não versionado)
- ✅ **Validação** de todos os inputs do usuário
- ✅ **Transações atômicas** com commit/rollback
- ✅ **Logging** de todas as operações em `sistema.log`
- ✅ **Pydantic** para validação automática de schemas na API

---

## 🧪 TESTES

### Rodar todos os testes
```bash
pytest tests/ -v
```

### Rodar testes com coverage
```bash
pytest tests/ -v --cov=. --cov-report=html
```

O relatório de coverage estará em `htmlcov/index.html`.

### Rodar apenas testes da API
```bash
pytest tests/test_api.py -v
```

---

## 🎯 BOAS PRÁTICAS

- **POO** — Classes `SistemaLoja` e `DatabaseManager` com responsabilidades bem definidas
- **DRY** — Código reutilizável com métodos específicos por operação
- **Separação de responsabilidades** — Módulos lógicos separados (db, validação, utils, API)
- **Tratamento de erros** — try/except em todas as operações críticas
- **Type hints** — Documentação de tipos em funções críticas
- **Testes automatizados** — Cobertura de validadores, utils e endpoints da API
- **CI/CD** — Pipeline automático com GitHub Actions

---

## 📊 ENDPOINTS DA API

### Produtos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/produtos/` | Criar produto |
| `GET` | `/api/v1/produtos/` | Listar todos os produtos |
| `GET` | `/api/v1/produtos/{id}` | Buscar produto por ID |
| `GET` | `/api/v1/produtos/busca/nome?nome=...` | Buscar por nome |
| `GET` | `/api/v1/produtos/busca/faixa-preco?min=...&max=...` | Buscar por faixa de preço |
| `PUT` | `/api/v1/produtos/{id}` | Atualizar produto |
| `DELETE` | `/api/v1/produtos/{id}` | Excluir produto |

### Vendas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/vendas/` | Registrar venda |
| `GET` | `/api/v1/vendas/` | Listar todas as vendas |
| `GET` | `/api/v1/vendas/{id}` | Buscar venda por ID |
| `GET` | `/api/v1/vendas/relatorio/periodo` | Relatório por período |
| `PUT` | `/api/v1/vendas/{id}` | Atualizar venda |
| `DELETE` | `/api/v1/vendas/{id}` | Excluir venda |

### Health Check
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Status da API |

---

## 🚀 CI/CD PIPELINE

O projeto possui pipeline automático que executa:

1. **Testes** em Python 3.10, 3.11 e 3.12
2. **Coverage** com relatório automático
3. **Build Docker** da imagem da API
4. **Deploy** (configurável)

Status do pipeline: ![CI/CD](https://github.com/LuizGSN/Gestao-loja/actions/workflows/ci-cd.yml/badge.svg)

---

## 📝 LICENÇA

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

---

## 👨‍💻 AUTOR

**Luiz Gonzaga**  
Estudante de Análise e Desenvolvimento de Sistemas

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?logo=github)](https://github.com/LuizGSN)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?logo=linkedin)](https://linkedin.com/in/luizgonzaga)

---

*⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!*
