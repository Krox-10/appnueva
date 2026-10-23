import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from jwt import InvalidTokenError

load_dotenv()

ALGORITHM = "HS256"
TOKEN_LIFETIME_HOURS = 8
TOKEN_LIFETIME_DAYS = 30


def crear_token_acceso(usuario, recordar=False):
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY no está configurada")

    ahora = datetime.now(timezone.utc)
    duracion = (
        timedelta(days=TOKEN_LIFETIME_DAYS)
        if recordar
        else timedelta(hours=TOKEN_LIFETIME_HOURS)
    )
    claims = {
        "sub": str(usuario["id_usuario"]),
        "id_rol": usuario["id_rol"],
        "rol": usuario["nombre_rol"],
        "iat": ahora,
        "exp": ahora + duracion,
    }
    token = jwt.encode(claims, secret_key, algorithm=ALGORITHM)
    return token, int(duracion.total_seconds())


def decodificar_token(token):
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY no está configurada")

    claims = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    if not claims.get("sub") or not claims.get("id_rol") or not claims.get("rol"):
        raise InvalidTokenError("Faltan datos de autenticación en el token")
    return claims