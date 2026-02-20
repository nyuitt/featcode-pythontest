"""
MAIN.PY — Ponto de entrada da aplicação FastAPI

Responsabilidades DESTE arquivo:
  1. Criar a instância do app
  2. Configurar metadados (título, versão, docs)
  3. Registrar os routers de cada domínio
  4. Adicionar middlewares globais (CORS, etc.)

O que NÃO fica aqui: lógica de negócio, queries, validações.
Se main.py crescer demais, algo está errado na arquitetura.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter
from app.routes import users
from app.routes import categories
from app.routes import products
from app.routes import dashboard

app = FastAPI(
    title="Featcode API",
    description="API de gestão de produtos — Desafio Técnico Featcode",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# CORS — permite que o frontend (localhost:5173) acesse a API (localhost:8000)
# Em produção: substitua origins por domínios reais e remova "*"
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# REGISTRO DE ROUTERS
# Cada domínio da aplicação tem seu próprio router.
# Aqui apenas os conectamos ao app principal.
# Para adicionar um novo domínio: crie o router e inclua aqui.
# ---------------------------------------------------------------------------
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(dashboard.router)



@app.get("/", tags=["Health"])
def health_check():
    """Endpoint de saúde — usado pelo Docker e load balancers."""
    return {"status": "ok", "version": "0.1.0"}
