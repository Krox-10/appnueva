from fastapi import FastAPI, HTTPException
from app.api import rutas_roles
from app.api import rutas_usuarios
from app.api import rutas_lineas
from app.api import rutas_semilleros
from app.api import rutas_investigaciones
from app.api import rutas_investigacion_miembros
from app.api import rutas_reuniones
from app.api import rutas_asistencia_reunion
from app.api import rutas_productos
from app.api import rutas_recursos
from app.api import rutas_modulos
from app.api import rutas_modulos_x_rol
from app.api import rutas_dashboard
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.auth import decodificar_token
from app.core.permissions import verificar_permiso

app = FastAPI(
    title="API de Gestión de Semilleros de Investigación",
    description="Backend modular para gestión de semilleros usando FastAPI y PostgreSQL.",
    version="1.0.0"
)

@app.middleware("http")
async def validar_autenticacion(request: Request, call_next):
    rutas_publicas = {
        "/",
        "/usuarios/login",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/oauth2-redirect",
    }

    if request.method == "OPTIONS" or request.url.path in rutas_publicas:
        return await call_next(request)

    authorization = request.headers.get("Authorization", "")
    esquema, _, token = authorization.partition(" ")
    if esquema.lower() != "bearer" or not token:
        token = request.cookies.get("access_token")

    if not token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Se requiere un token de acceso válido"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        request.state.usuario = decodificar_token(token)
    except RuntimeError:
        return JSONResponse(
            status_code=500,
            content={"detail": "La autenticación no está configurada en el servidor"},
        )
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"detail": "El token es inválido o ha expirado"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        verificar_permiso(request, request.state.usuario)
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail},
        )

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rutas_roles.router)
app.include_router(rutas_usuarios.router)
app.include_router(rutas_lineas.router)
app.include_router(rutas_semilleros.router)
app.include_router(rutas_investigaciones.router)
app.include_router(rutas_investigacion_miembros.router)
app.include_router(rutas_reuniones.router)
app.include_router(rutas_asistencia_reunion.router)
app.include_router(rutas_productos.router)
app.include_router(rutas_recursos.router)
app.include_router(rutas_modulos.router)
app.include_router(rutas_modulos_x_rol.router)
app.include_router(rutas_dashboard.router)
@app.get("/")
def estado_api():
    return {
        "mensaje": "La API de gestión de semilleros se encuentra en línea y funcional"
    }