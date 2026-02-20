"""
ROTAS DE USUÁRIOS — Por que tão limpas?

As rotas têm UMA única responsabilidade: orquestrar.
Elas recebem a requisição HTTP, delegam para o CRUD, e formatam a resposta.
Nenhuma query SQL aqui. Nenhuma regra de negócio complexa aqui.

Por que usar APIRouter em vez de colocar tudo no main.py?
- Organização: cada domínio (users, products, categories) tem seu próprio arquivo
- Prefixos e tags são declarados uma vez por router, não em cada rota
- main.py fica limpo — só registra routers, não define rotas

Por que response_model=UserResponse?
- FastAPI serializa automaticamente o objeto SQLAlchemy para JSON
  usando o schema Pydantic definido
- Filtra campos que não devem aparecer na resposta (ex: keycloak_id)
- Documenta o contrato da API no Swagger automaticamente
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate, UserResponse

# prefix: todas as rotas deste router terão /users como base
# tags: agrupa no Swagger UI — melhora muito a navegabilidade da doc
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def create_user(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário.

    Por que checamos duplicidade aqui e não no CRUD?
    Porque é uma REGRA DE NEGÓCIO ("email único"), não uma operação de banco.
    O CRUD poderia receber a mesma chamada de múltiplos contextos
    (API, worker, teste) — cada um decide como tratar o conflito.
    """
    existing = crud_user.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Usuário com email '{user_in.email}' já existe."
        )
    return crud_user.create_user(db, user_in=user_in)


@router.get("/", response_model=list[UserResponse])
@limiter.limit("100/minute")
def list_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista usuarios com paginação simples.
    skip e limit viram query params automaticamente: GET /users?skip=0&limit=10
    """
    return crud_user.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("100/minute")
def get_user(request: Request, user_id: str, db: Session = Depends(get_db)):
    """
    Busca um usuário pelo ID.
    Retorna 404 se não encontrado — nunca retornamos None na API, sempre HTTP semântico.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário '{user_id}' não encontrado."
        )
    return db_user


@router.patch("/{user_id}", response_model=UserResponse)
@limiter.limit("30/minute")
def update_user(request: Request, user_id: str, user_in: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualização parcial (PATCH).
    Primeiro busca, depois verifica existência, depois delega para o CRUD.
    Essa sequência — busca → valida → opera — é o padrão correto.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário '{user_id}' não encontrado."
        )
    return crud_user.update_user(db, db_user=db_user, user_in=user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("20/minute")
def delete_user(request: Request, user_id: str, db: Session = Depends(get_db)):
    """
    Deleta um usuário.
    204 No Content é o código HTTP correto para DELETE bem-sucedido.
    Não retornamos body — o status code já comunica o resultado.
    """
    deleted = crud_user.delete_user(db, user_id=user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário '{user_id}' não encontrado."
        )
