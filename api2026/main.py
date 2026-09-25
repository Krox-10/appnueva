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

app = FastAPI(
    title="API de Gestión de Semilleros de Investigación",
    description="Backend modular para gestión de semilleros usando FastAPI y PostgreSQL.",
    version="1.0.0"
)

# Conectamos los módulos de rutas a la aplicación principal
app.include_router(rutas_roles.router)
app.include_router(rutas_usuarios.router)
app.include_router(rutas_lineas.router)
app.include_router(rutas_semilleros.router)
app.include_router(rutas_investigaciones.router)
app.include_router(rutas_investigacion_miembros.router)
app.include_router(rutas_reuniones.router)
app.include_router(rutas_asistencias.router)
app.include_router(rutas_productos.router)

@app.get("/")
def estado_api():
    return {
        "mensaje": "La API de gestión de semilleros se encuentra en línea y funcional"
    }