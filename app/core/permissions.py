from fastapi import HTTPException, Request

from app.core.database import Database


ROLE_ADMIN = "administrador"

PERMISSIONS = {
    "/usuarios": {
        "GET": (
            "gestionar_usuarios",
            "consultar_miembros",
            "gestionar_miembros",
            "consultar_semilleros",
        ),
        "POST": ("gestionar_usuarios", "gestionar_miembros"),
        "PUT": ("gestionar_usuarios", "gestionar_miembros"),
        "DELETE": ("gestionar_usuarios", "gestionar_miembros"),
    },
    "/semilleros": {
        "GET": ("consultar_semilleros", "gestionar_semilleros"),
        "POST": ("gestionar_semilleros",),
        "PUT": ("gestionar_semilleros",),
        "DELETE": ("gestionar_semilleros",),
    },
    "/lineas-investigacion": {
        "GET": ("consultar_semilleros", "gestionar_semilleros"),
        "POST": ("gestionar_semilleros",),
        "PUT": ("gestionar_semilleros",),
        "DELETE": ("gestionar_semilleros",),
    },
    "/investigaciones": {
        "GET": ("consultar_investigaciones", "gestionar_investigaciones"),
        "POST": ("gestionar_investigaciones",),
        "PUT": ("gestionar_investigaciones",),
        "DELETE": ("gestionar_investigaciones",),
    },
    "/investigaciones-miembros": {
        "GET": ("consultar_investigaciones", "gestionar_investigaciones"),
        "POST": ("gestionar_investigaciones",),
        "PUT": ("gestionar_investigaciones",),
        "DELETE": ("gestionar_investigaciones",),
    },
    "/reuniones": {
        "GET": ("consultar_reuniones", "agendar_reuniones"),
        "POST": ("agendar_reuniones",),
        "PUT": ("agendar_reuniones",),
        "DELETE": ("agendar_reuniones",),
    },
    "/asistencia_reunion": {
        "GET": ("consultar_reuniones", "agendar_reuniones"),
        "POST": ("consultar_reuniones", "agendar_reuniones"),
        "PUT": ("consultar_reuniones", "agendar_reuniones"),
        "DELETE": ("consultar_reuniones", "agendar_reuniones"),
    },
    "/productos-investigacion": {
        "GET": ("consultar_productos", "subir_productos"),
        "POST": ("subir_productos",),
        "PUT": ("subir_productos",),
        "DELETE": ("subir_productos",),
    },
    "/recursos-semillero": {
        "GET": ("gestionar_semilleros", "gestionar_recursos"),
        "POST": ("gestionar_semilleros", "gestionar_recursos"),
        "PUT": ("gestionar_semilleros", "gestionar_recursos"),
        "DELETE": ("gestionar_semilleros", "gestionar_recursos"),
    },
    "/dashboard": {
        "GET": (
            "consultar_semilleros",
            "gestionar_semilleros",
            "consultar_reuniones",
            "agendar_reuniones",
            "consultar_investigaciones",
            "gestionar_investigaciones",
            "gestionar_usuarios",
            "consultar_miembros",
        ),
    },
}


def _permission_for(request: Request):
    path = request.url.path.rstrip("/") or "/"
    method = request.method.upper()

    if path == "/usuarios/logout":
        return None, "authenticated"

    if path.startswith("/usuarios/") and method == "GET":
        return None, "administrator"

    if path.startswith("/modulos-x-rol/rol/"):
        return None, "role_modules"

    for prefix, methods in PERMISSIONS.items():
        if path == prefix or path.startswith(f"{prefix}/"):
            return methods.get(method), "module"

    if path.startswith(("/roles", "/modulos", "/modulos-x-rol")):
        return None, "administrator"

    return None, "authenticated"


def verificar_permiso(request: Request, usuario: dict):
    rol = str(usuario.get("rol", "")).strip().casefold()
    if rol == ROLE_ADMIN:
        return

    modulos_requeridos, tipo = _permission_for(request)

    if tipo == "administrator":
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")

    if tipo == "role_modules":
        role_id = request.url.path.rstrip("/").split("/")[-1]
        if role_id != str(usuario.get("id_rol")):
            raise HTTPException(status_code=403, detail="No puedes consultar módulos de otro rol")
        return

    if tipo == "authenticated":
        return

    if not modulos_requeridos:
        raise HTTPException(status_code=403, detail="No hay permisos configurados para esta operación")

    db = Database()
    conn = db.get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No fue posible conectar con la base de datos")

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM modulosxrol mxr
                INNER JOIN modulos m ON m.id_modulo = mxr.id_modulo
                WHERE mxr.id_rol = %s
                  AND mxr.estado = TRUE
                  AND m.estado = TRUE
                  AND m.nombre = ANY(%s)
            ) AS permitido;
            """,
            (usuario.get("id_rol"), list(modulos_requeridos)),
        )
        if not cursor.fetchone()["permitido"]:
            raise HTTPException(status_code=403, detail="Tu rol no tiene permiso para esta operación")
    finally:
        conn.close()