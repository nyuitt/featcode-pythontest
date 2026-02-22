from functools import lru_cache
from typing import Any

import httpx
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwk, jwt
from jose.utils import base64url_decode

log = structlog.get_logger("auth")

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "featcode"
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def _get_jwks() -> list[dict]:
    try:
        response = httpx.get(JWKS_URL, timeout=5)
        response.raise_for_status()
        return response.json()["keys"]
    except Exception as exc:
        log.error("auth.jwks_fetch_failed", error=str(exc))
        return []


def _get_public_key(token: str) -> Any:
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    keys = _get_jwks()
    for key_data in keys:
        if key_data.get("kid") == kid:
            return jwk.construct(key_data)
    return None


def verify_token(token: str) -> dict:
    try:
        public_key = _get_public_key(token)
        if public_key is None:
            _get_jwks.cache_clear()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Chave pública não encontrada. Tente novamente.",
            )
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload
    except JWTError as exc:
        log.warning("auth.token_invalid", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return verify_token(credentials.credentials)
