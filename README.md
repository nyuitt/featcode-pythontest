# Desafio Técnico Featcode - Sistema de Gestão de Produtos

## Visão Geral

Bem-vindo ao desafio técnico da Feat! Este projeto consiste no desenvolvimento de um sistema completo de gestão de produtos, demonstrando suas habilidades em arquitetura moderna, boas práticas de desenvolvimento e tecnologias de ponta.

## Referência Visual

O design da aplicação deve seguir o padrão visual moderno demonstrado neste protótipo:

**ShopSense Dashboard - Product Page**: https://dribbble.com/shots/24351485-ShopSense-Sales-Dashboard

## Requisitos do Sistema

### Funcionalidades Principais

#### Gestão de Produtos
- Criar, listar, editar e excluir produtos
- Cada produto deve conter: nome, descrição, preço, categoria, quantidade em estoque
- Validação básica de dados obrigatórios
- Busca simples por nome do produto

#### Sistema de Categorias
- Criar e gerenciar categorias de produtos (lista simples)
- Associar produtos a uma categoria
- Filtrar produtos por categoria

#### Controle de Estoque
- Controlar quantidade em estoque de cada produto
- Atualização manual de estoque
- Exibir produtos com estoque baixo (menor que 10 unidades)

#### Dashboard Simples
- Total de produtos cadastrados
- Valor total do estoque
- Lista de produtos com estoque baixo
- Gráfico básico de produtos por categoria

#### Sistema de Autenticação
- Integração com **Keycloak** para autenticação
- Login via Keycloak (OAuth2/OpenID Connect)
- Proteção de rotas no frontend
- Autorização baseada em roles do Keycloak
- Logout integrado com Keycloak

### Requisitos Técnicos

#### Performance
- Resposta da API em menos de 500ms para consultas simples
- Paginação eficiente para grandes volumes
- Cache para consultas frequentes
- Otimização de queries no banco

#### Escalabilidade
- Arquitetura preparada para crescimento horizontal
- Separação clara entre camadas
- Padrões que facilitem manutenção e evolução
- Código limpo e bem estruturado

#### Segurança
- Rate limiting para prevenir abuso
- Validação e sanitização de entradas
- Headers de segurança adequados
- Tratamento seguro de dados sensíveis

#### Disponibilidade
- Health checks implementados
- Tratamento adequado de erros
- Mensagens de erro claras e úteis
- Logs estruturados para monitoramento

#### Usabilidade
- Interface responsiva (desktop e mobile)
- Validação em tempo real nos formulários
- Feedback visual para ações do usuário
- Experiência intuitiva e consistente

## Stack Tecnológica

### Frontend
- **React 18** com TypeScript
- **Vite** ou **Next.js 14** (App Router)
- **TailwindCSS** + **Shadcn/ui** para estilização
- **React Query/TanStack Query** para gerenciamento de estado
- **React Hook Form** + **Zod** para validação
- **Recharts** ou **Chart.js** para dashboards
- **React Testing Library** + **Vitest** para testes


### Backend
- **Python** com **FastAPI**
- **Clean Architecture** + **DDD** (Domain-Driven Design)
- **CQRS** + **mediatr** pattern
- **PostgreSQL** como banco principal
- **Pydantic v2** para validação e mapeamento de dados
- **SQLAlchemy** + **Alembic** para ORM e migrations
- **structlog** ou **loguru** para logging estruturado
- **pytest** + **pytest-asyncio** + **httpx** para testes

### Infraestrutura
- **Postgress** como banco principal
- **Keycloak** para autenticação e autorização
- **Docker** + **Docker Compose** para containerização
- **Nginx** como reverse proxy

## Arquitetura do Sistema

### Backend - Clean Architecture + DDD

```
src/
├── domain/                      # Camada de Domínio
│   ├── entities/                # Entidades do domínio
│   ├── value_objects/           # Objetos de valor
│   ├── events/                  # Eventos de domínio
│   ├── repositories/            # Interfaces dos repositórios (ABC)
│   └── services/                # Serviços de domínio
├── application/                 # Camada de Aplicação
│   ├── commands/                # Comandos CQRS
│   ├── queries/                 # Consultas CQRS
│   ├── handlers/                # Handlers (mediatr)
│   ├── schemas/                 # Schemas Pydantic (DTOs)
│   ├── validators/              # Validadores Pydantic
│   └── interfaces/              # Interfaces da aplicação (ABC)
├── infrastructure/              # Camada de Infraestrutura
│   ├── database/                # Configurações SQLAlchemy + Alembic
│   ├── repositories/            # Implementação dos repositórios
│   ├── services/                # Serviços externos
│   └── config/                  # Configurações de injeção de dependência
└── api/                         # Camada de Apresentação
    ├── routers/                 # Routers FastAPI
    ├── middlewares/             # Middlewares customizados
    ├── dependencies/            # Dependências FastAPI (Depends)
    └── exceptions/              # Handlers de exceção
```

### Frontend - Arquitetura Modular

```
src/
├── components/                   # Componentes reutilizáveis
│   ├── ui/                      # Componentes base (shadcn/ui)
│   ├── forms/                   # Componentes de formulário
│   ├── charts/                  # Componentes de gráficos
│   └── layout/                  # Componentes de layout
├── pages/                       # Páginas da aplicação
├── hooks/                       # Custom hooks
├── services/                    # Serviços de API
├── stores/                      # Stores de estado global
├── types/                       # Definições de tipos
├── utils/                       # Funções utilitárias
└── lib/                         # Configurações de bibliotecas
```

## Diferenciais

#### Testes Abrangentes
- Cobertura mínima de 85% no backend
- Testes E2E com **Playwright** (pytest-playwright)
- Testes de integração para todos os endpoints com **httpx** + **pytest-asyncio**
- Testes unitários para regras de negócio com **pytest**
- Testes de mutação com **mutmut** para validar qualidade

#### Observabilidade Completa
- Logs estruturados com correlationId via **structlog** ou **loguru**
- Métricas customizadas com **prometheus-fastapi-instrumentator**
- Health checks detalhados via endpoint `/health` (FastAPI)
- Tratamento adequado de erros com contexto
- Monitoring de performance com **OpenTelemetry**

#### Performance e Otimização
- Server-side rendering (Next.js)
- Code splitting e lazy loading
- Estratégias de caching (Redis + HTTP cache)
- Indexação otimizada do banco de dados
- Otimização de imagens e assets
- Compressão de responses

#### Segurança Avançada
- Integração completa com Keycloak
- Proteção de rotas baseada em roles
- Token JWT validado adequadamente
- CORS configurado adequadamente
- Headers de segurança implementados
- Validação em múltiplas camadas

#### Qualidade de Código
- Princípios SOLID aplicados consistentemente
- Clean Code em todas as camadas
- Padrões de design bem implementados
- Documentação inline adequada
- Tratamento de exceções robusto

#### Documentação Excepcional
- OpenAPI/Swagger com exemplos detalhados
- Documentação de arquitetura (C4 Model)
- ADRs (Architecture Decision Records)
- Guias de instalação e execução completos
- Collection do Postman atualizada

### Pontos Extras (Opcionais)

- **Roles avançadas no Keycloak** (Admin, Manager, User)
- **GraphQL** como alternativa à REST API via **Strawberry** (FastAPI)
- **Real-time updates** via **WebSockets** nativos do FastAPI
- **Exportação de relatórios** em PDF via **WeasyPrint** ou **ReportLab**
- **Internacionalização** (i18n) básica com **Babel**
- **PWA** com capacidades offline
- **Docker multi-stage builds** otimizados

## Como Executar

### Pré-requisitos
- Docker Desktop 4.0+
- Node.js 18+
- Python 3.11+
- Git

### Instalação e Execução

```bash
# Clone o repositório
git clone [https://github.com/featcodetecnologia/desafio-01/]


# Copie as variáveis de ambiente
cp .env.example .env

# Execute toda a aplicação com Docker Compose
docker-compose up -d

# Aguarde alguns segundos para os serviços iniciarem
# Verifique se todos os containers estão rodando
docker-compose ps
```

### URLs de Acesso
- **Frontend**: http://localhost:3000
- **API**: http://localhost:5000
- **Swagger**: http://localhost:5000/swagger
- **Postgres**: http://localhost:5432
- **Keycloak**: http://localhost:8080

### Desenvolvimento Local

```bash
# Para desenvolvimento do frontend
cd frontend
npm install
npm run dev

# Para desenvolvimento do backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload

# Para executar testes
pytest --cov=src --cov-report=term-missing
cd ../frontend
npm test
```

## Padrões de Commit

Este projeto utiliza [Conventional Commits](https://conventionalcommits.org/):

```bash
# Exemplos de commits
feat(products): add bulk import functionality
fix(api): resolve pagination issue in products endpoint
docs(readme): update installation instructions
test(products): add unit tests for product service
refactor(auth): improve JWT token validation
perf(database): optimize product search queries
style(frontend): apply consistent spacing in components
chore(deps): update dependencies to latest versions
```

### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, ponto e vírgula, etc
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Tarefas de manutenção
- `perf`: Melhorias de performance
- `build`: Build e dependências

## Critérios de Avaliação

### Técnico (60%)
- **Arquitetura**: Clean Architecture, DDD, CQRS implementados corretamente
- **Qualidade de Código**: SOLID, Clean Code, padrões consistentes
- **Testes**: Cobertura, qualidade dos testes, cenários bem cobertos
- **Performance**: Otimizações, caching, queries eficientes
- **Segurança**: Implementação adequada de autenticação/autorização

### Funcional (25%)
- **Completude**: Todas as funcionalidades implementadas
- **UX/UI**: Interface intuitiva e responsiva
- **Validações**: Tratamento adequado de erros
- **Regras de Negócio**: Implementação correta dos requisitos

### Profissional (15%)
- **Documentação**: README completo, código bem documentado
- **Git Flow**: Commits organizados, branches bem estruturadas
- **Docker**: Compose funcionando perfeitamente
- **Extras**: Funcionalidades que demonstram expertise avançada

## Entregáveis

### Código Fonte
- Repositório GitHub público
- README detalhado (este arquivo)
- Docker Compose funcional
- Testes automatizados com boa cobertura

### Aplicação Funcionando
- Todos os serviços rodando via Docker Compose
- Banco de dados populado com dados de exemplo
- Interface funcional e responsiva

### Documentação
- API documentada com Swagger
- Guia de instalação e execução
- Documentação das decisões arquiteturais

### Apresentação
- Vídeo de 5-10 minutos demonstrando a aplicação
- Explicação das decisões técnicas tomadas
- Showcase das funcionalidades implementadas
- Demonstração dos diferenciais implementados


---

**Boa sorte e mostre do que você é capaz!**

---

*Este desafio foi criado para identificar desenvolvedores excepcionais que compartilham nossa paixão por tecnologia e excelência técnica. Estamos ansiosos para ver sua solução!*
