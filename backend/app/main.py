"""
MAIN.PY — Ponto de entrada da aplicação FastAPI

Responsabilidades DESTE arquivo:
  1. Criar a instância do app
  2. Configurar metadados (título, versão, docs)
  3. Registrar os routers de cada domínio
  4. Adicionar middlewares globais (CORS, logging, rate limiting)

O que NÃO fica aqui: lógica de negócio, queries, validações.
Se main.py crescer demais, algo está errado na arquitetura.
"""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter
from app.core.logging import configure_logging
from app.middleware.logging_middleware import LoggingMiddleware
from app.routes import users
from app.routes import categories
from app.routes import products
from app.routes import dashboard


configure_logging()

log = structlog.get_logger("app")

app = FastAPI(
    title="Featcode API",
    description="API de gestão de produtos — Desafio Técnico Featcode",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
# LoggingMiddleware fica por fora do CORSMiddleware para logar também erros CORS.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# ---------------------------------------------------------------------------
# REGISTRO DE ROUTERS
# ---------------------------------------------------------------------------
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def on_startup():
    log.info("app.startup", version="0.1.0", environment="development")


@app.get("/", tags=["Health"])
def health_check():
    """Endpoint de saúde — usado pelo Docker e load balancers."""
    return {"status": "ok", "version": "0.1.0"}
