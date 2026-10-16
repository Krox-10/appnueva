from fastapi import FastAPI
from app.api import rutas_roles
from app.api import rutas_usuarios
from app.api import rutas_lineas
from app.api import rutas_semilleros
from app.api import rutas_investigaciones
from app.api import rutas_investigacion_miembros
from app.api import rutas_reuniones
from app.api import rutas_asistencias
from app.api import rutas_productos
from app.api import rutas_recursos
from app.api import rutas_modulos
from app.api import rutas_modulos_x_rol
from app.api import rutas_dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Gestión de Semilleros de Investigación",
    description="Backend modular para gestión de semilleros usando FastAPI y PostgreSQL.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5176",
    "http://127.0.0.1:5176"
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
app.include_router(rutas_asistencias.router)
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