"""
SCHEMAS DE USUÁRIO — Por que existem?

O Model SQLAlchemy (User) representa a TABELA no banco.
Os Schemas Pydantic representam os DADOS que trafegam pela API.

Por que separar?
- O model pode ter campos sensíveis (senha_hash, keycloak_id) que
  nunca devem ser expostos na API.
- A validação de entrada (ex: email válido, nome obrigatório) é
  responsabilidade do schema, não do model.
- Você pode ter shapes diferentes: criar usuário precisa de campos X,
  retornar usuário expõe campos Y. Com um único model, isso seria impossível.
"""

from pydantic import BaseModel, EmailStr, Field
import uuid


class UserBase(BaseModel):
    """
    Campos compartilhados entre criação e resposta.
    Herde desta classe para evitar repetição (DRY).
    """
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    """
    Schema de ENTRADA para criar um usuário via POST /users.
    Herda email e full_name de UserBase.
    Adicionamos keycloak_id opcional — pode vir do token JWT futuramente.

    Por que separar do UserResponse?
    Porque na criação podemos aceitar campos que nunca devolvemos
    (ex: senha em texto puro antes de hashear).
    """
    keycloak_id: str | None = None


class UserUpdate(BaseModel):
    """
    Schema de ENTRADA para atualizar — todos os campos são opcionais.
    PATCH semântico: só atualiza o que foi enviado.

    Por que não reutilizar UserCreate? Porque no update, nenhum campo
    é obrigatório. Forçar full_name obrigatório num PATCH seria errado.
    """
    full_name: str | None = Field(None, min_length=2, max_length=255)
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema de SAÍDA — o que a API retorna.
    Note: keycloak_id e campos internos ficam fora por segurança.

    from_attributes=True é a forma Pydantic v2 de dizer que pode
    transformar um objeto SQLAlchemy (ORM) em schema Pydantic.
    Antes era orm_mode=True (Pydantic v1).
    """
    id: str
    is_active: bool

    model_config = {"from_attributes": True}
