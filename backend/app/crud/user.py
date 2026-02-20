"""
CAMADA CRUD — Por que existe?

Sem essa camada, as rotas fariam queries SQL diretamente:
    @router.get("/users")
    def list_users(db: Session = Depends(get_db)):
        return db.query(User).all()  # ← lógica de BD vaza na rota

Problemas dessa abordagem:
1. Impossível testar sem banco de dados — a rota e a query são inseparáveis.
2. Duplicação: se outra rota precisar da mesma query, você copia o código.
3. Viola Single Responsibility: a rota deveria apenas orquestrar, não queryar.

Com a camada CRUD:
- Rotas ficam limpas (recebem dados, chamam crud.xxx, devolvem resultado)
- Queries ficam centralizadas e testáveis isoladamente
- Reusar a mesma lógica de acesso ao banco em múltiplos lugares
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
import uuid


def get_user(db: Session, user_id: str) -> User | None:
    """
    Busca um único usuário por ID.
    Retorna None se não existir — quem decide o que fazer com None é a rota.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca por email — útil para checar duplicidade antes de criar.
    """
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Lista usuários com paginação simples (offset/limit).
    skip=0, limit=100 são defaults razoáveis para desenvolvimento.

    Para produção: considerar keyset pagination (mais eficiente em grandes volumes).
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Cria um novo usuário.

    Por que usamos model_dump() e não passamos o schema direto?
    Porque o model SQLAlchemy não conhece Pydantic.
    model_dump() converte o schema para dict Python puro.

    O ** desempacota o dict como keyword arguments para o construtor.
    """
    db_user = User(
        id=str(uuid.uuid4()),  # Geramos o ID aqui — não dependemos do banco
        **user_in.model_dump()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)   # Recarrega o objeto do banco (garante valores defaults do BD)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    """
    Atualização parcial (PATCH): só altera os campos enviados.

    exclude_unset=True é a chave aqui:
    Se o cliente enviar apenas {"full_name": "João"}, só full_name é atualizado.
    Sem isso, is_active seria sobrescrito com None e corromperia o registro.
    """
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> bool:
    """
    Deleta um usuário. Retorna True se deletou, False se não encontrou.
    A rota usa esse bool para decidir se retorna 200 ou 404.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
