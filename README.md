# Featcode — Sistema de Gestão de Produtos

> Desafio técnico implementado em Python/FastAPI com React, containerizado via Docker e com pipeline de testes automatizados.

---

## O que foi entregue

| Requisito | Status |
|---|---|
| CRUD de Produtos (nome, descrição, preço, categoria, estoque) | ✅ |
| CRUD de Categorias | ✅ |
| Busca por nome e filtro por categoria | ✅ |
| Controle de estoque + alerta de estoque baixo | ✅ |
| Dashboard (totais, valor de estoque, produtos por categoria) | ✅ |
| Paginação eficiente (skip/limit) | ✅ |
| Rate limiting (slowapi — 429 após limite atingido) | ✅ |
| Logging estruturado em JSON (structlog) | ✅ |
| Testes automatizados — 41 testes, 97% de cobertura | ✅ |
| Nginx como reverse proxy unificado | ✅ |
| Frontend React completo com Shadcn/ui e TanStack Query | ✅ |
| Migrações com Alembic | ✅ |
| Seed de dados realistas | ✅ |
| **Autenticação Keycloak (OAuth2/OIDC)** | ⏳ Pendente |

---

## Stack técnica

### Backend
- **Python 3.11** + **FastAPI** — framework escolhido pela performance (ASGI assíncrono), tipagem nativa via Pydantic e documentação OpenAPI automática
- **SQLAlchemy 2.0** (ORM) + **Alembic** (migrações) — abordagem code-first para o schema do banco
- **PostgreSQL 16** — banco principal; **SQLite** em memória apenas nos testes
- **slowapi** — rate limiting por IP baseado em janela deslizante
- **structlog** — logs em JSON estruturado, com `request_id` por request e logs de negócio nos CRUD operations
- **pytest** + **pytest-cov** + **httpx** — suite de testes com banco isolado por fixture

### Frontend
- **React 18** + **TypeScript** + **Vite**
- **TanStack Query** — cache e sincronização de estado com o servidor
- **React Hook Form** + **Zod** — validação de formulários com tipagem end-to-end
- **Shadcn/ui** — componentes acessíveis sobre Radix UI
- **Recharts** — gráfico de produtos por categoria no dashboard

### Infraestrutura
- **Docker Compose** com 5 serviços: `postgres`, `keycloak`, `backend`, `frontend`, `nginx`
- **Nginx** como reverse proxy: `/api/*` → backend (8000), `/*` → frontend (5173)
- Hot-reload em desenvolvimento para ambos os serviços

---

## Decisões de arquitetura

### Separação de responsabilidades
O backend segue uma arquitetura em camadas explícita:

```
routes/      ← recebe HTTP, delega, retorna resposta
crud/        ← operações de banco (sem lógica de negócio)
schemas/     ← contratos de entrada e saída (Pydantic)
models/      ← mapeamento ORM → tabelas
core/        ← configurações transversais (DB, limiter, logging)
middleware/  ← logging de requests
```

Cada camada conhece apenas a camada imediatamente abaixo. Rotas não fazem queries SQL; CRUDs não conhecem HTTP.

### Por que FastAPI e não Django REST?
FastAPI oferece tipagem nativa, validação automática via Pydantic, documentação OpenAPI gerada sem esforço e suporte a async por padrão. Para uma API REST com foco em performance e developer experience, é a escolha mais adequada no ecossistema Python atual.

### Por que Pydantic schemas separados do model ORM?
Os modelos SQLAlchemy representam tabelas. Os schemas Pydantic representam o contrato da API. Separar os dois permite:
- Ocultar campos sensíveis (ex: `keycloak_id`) da resposta
- Ter shapes diferentes para criação (`UserCreate`) e resposta (`UserResponse`)
- Validar entrada antes de qualquer operação no banco

### Logging estruturado
Todo request gera um log JSON com `request_id`, método, path, status e duração. Isso permite correlacionar logs de uma mesma requisição em ferramentas como Grafana Loki, Datadog ou ELK. Operações de negócio (criação, atualização, deleção) geram eventos adicionais para auditoria.

### Estratégia de testes
Os testes usam **SQLite em memória** com um `conftest.py` central que:
1. Cria o schema completo antes de cada teste
2. Destrói tudo após o teste (isolamento total)
3. Sobrescreve a dependency `get_db` do FastAPI via `dependency_overrides`

Essa abordagem não depende de nenhum serviço externo rodando — os 41 testes executam em ~1 segundo.

---

## Como rodar

### Pré-requisitos
- Docker
- Docker Compose

### 1. Subir os serviços
```bash
docker compose up -d
```

Aguardar ~15 segundos para o PostgreSQL inicializar.

### 2. Executar as migrações
```bash
docker exec featcode_backend alembic upgrade head
```

### 3. Popular o banco com dados iniciais (opcional)
```bash
docker exec featcode_backend python seed.py
```

Seed inclui 5 categorias e 20 produtos realistas, alguns com estoque propositalmente baixo para demonstrar os alertas do dashboard.

### 4. Acessar a aplicação
| Serviço | URL |
|---|---|
| **Frontend** | http://localhost |
| **API** | http://localhost/api |
| **Swagger UI** | http://localhost:8000/docs |
| **Keycloak Admin** | http://localhost:8081 (admin/admin) |

---

## Como executar os testes

```bash
# Rodar a suite completa com relatório de cobertura
docker exec featcode_backend bash -c "cd /app && python -m pytest tests/ -v --cov=app --cov-report=term-missing"
```

Resultado esperado:
```
41 passed in ~1.1s
TOTAL    463    14    97%
```

### Estrutura dos testes
```
backend/tests/
├── conftest.py          # fixtures: TestClient + banco SQLite isolado
├── test_health.py       # smoke test do endpoint raiz
├── test_categories.py   # 10 testes: CRUD completo + conflitos + 404s
├── test_products.py     # 17 testes: CRUD + busca + filtros + paginação + estoque baixo
├── test_dashboard.py    # 3 testes: estado vazio + dados reais + cálculo de métricas
└── test_users.py        # 10 testes: CRUD completo + email duplicado + 404s
```

---

## Endpoints da API

### Produtos
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/products/` | Lista produtos (suporta `search`, `category_id`, `skip`, `limit`) |
| `POST` | `/products/` | Cria produto |
| `GET` | `/products/{id}` | Busca por ID |
| `PATCH` | `/products/{id}` | Atualização parcial |
| `PATCH` | `/products/{id}/stock` | Atualiza estoque |
| `DELETE` | `/products/{id}` | Remove produto |
| `GET` | `/products/low-stock` | Lista produtos com estoque < 10 |

### Categorias
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/categories/` | Lista categorias |
| `POST` | `/categories/` | Cria categoria |
| `GET` | `/categories/{id}` | Busca por ID |
| `PATCH` | `/categories/{id}` | Atualização parcial |
| `DELETE` | `/categories/{id}` | Remove categoria |

### Dashboard
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/dashboard/` | Retorna métricas agregadas |

### Usuários
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/users/` | Lista usuários |
| `POST` | `/users/` | Cria usuário |
| `GET` | `/users/{id}` | Busca por ID |
| `PATCH` | `/users/{id}` | Atualização parcial |
| `DELETE` | `/users/{id}` | Remove usuário |

---

## Rate Limiting

Todas as rotas possuem limites por IP via `slowapi`. Quando o limite é excedido, a API retorna `HTTP 429 Too Many Requests`.

| Tipo de operação | Limite |
|---|---|
| Leituras (GET) | 100 req/min |
| Escritas (POST/PATCH/DELETE) | 30 req/min |
| Dashboard | 60 req/min |
| Criação/deleção de usuário | 20 req/min |

---

## O que está pendente

### Autenticação com Keycloak
O container do Keycloak já sobe junto com o `docker compose up`, mas a integração com a API ainda não foi implementada. O que faltaria:
- Middleware de validação de token JWT no backend
- Dependency `require_auth` para proteger rotas
- Fluxo de login no frontend (redirect OAuth2, armazenamento de token, envio no header)

### Tratamento global de erros
Exceções não tratadas atualmente retornam o erro padrão do FastAPI (500). Seria necessário um exception handler centralizado com respostas padronizadas.

---

## Estrutura do projeto

```
.
├── backend/
│   ├── app/
│   │   ├── core/          # database, limiter, logging
│   │   ├── crud/          # operações de banco
│   │   ├── middleware/    # logging_middleware
│   │   ├── models/        # SQLAlchemy ORM
│   │   ├── routes/        # FastAPI routers
│   │   └── schemas/       # Pydantic schemas
│   ├── alembic/           # migrações
│   ├── tests/             # suite de testes
│   ├── seed.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/    # UI components (Shadcn)
│       ├── pages/         # Dashboard, Products, Categories
│       └── services/      # axios client
├── nginx/
│   └── nginx.conf
└── docker-compose.yml
```
