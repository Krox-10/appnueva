import os

from fastapi import APIRouter, HTTPException, Request, Response
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
from pydantic import BaseModel
from app.core.database import Database
from app.core.auth import crear_token_acceso
from app.core.passwords import hash_password, verify_password

class LoginRequest(BaseModel):
    correo: str
    contrasena: str
    rol: str
    recordar: bool = False

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"]
)

repo = UsuarioRepository()


@router.get("/")
def listar_usuarios(request: Request):
    usuarios = repo.obtener_todos()
    rol = str(request.state.usuario.get("rol", "")).strip().casefold()

    if rol == "estudiante":
        return [
            {
                "id_usuario": usuario["id_usuario"],
                "id_semillero": usuario["id_semillero"],
                "estado": usuario["estado"],
            }
            for usuario in usuarios
        ]

    return usuarios


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return repo.obtener_por_id(usuario_id)


@router.post("/")
def crear_usuario(usuario: Usuario):
    if not usuario.contrasena:
        raise HTTPException(status_code=422, detail="La contraseña es obligatoria")

    nuevo_id = repo.crear(usuario)

    return {
        "mensaje": "Usuario registrado exitosamente",
        "id": nuevo_id
    }


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    repo.eliminar(usuario_id)

    return {
        "mensaje": "Usuario desactivado correctamente"
    }


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario):
    if usuario.contrasena == "":
        raise HTTPException(status_code=422, detail="La contraseña no puede estar vacía")

    repo.actualizar(usuario_id, usuario)

    return {
        "mensaje": "Usuario actualizado correctamente"
    }

@router.post("/login")
def iniciar_sesion(datos: LoginRequest, response: Response):
    db = Database()
    conn = db.get_connection()

    if conn is None:
        raise HTTPException(
            status_code=500,
            detail="No fue posible conectar con la base de datos"
        )

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                u.id_usuario,
                u.nombre_usuario,
                u.correo,
                u.contrasena,
                u.id_rol,
                r.nombre AS nombre_rol
            FROM usuario u
            INNER JOIN rol r ON r.id_rol = u.id_rol
            WHERE LOWER(TRIM(u.correo)) = LOWER(TRIM(%s))
              AND u.estado = TRUE
              AND r.estado = TRUE;
        """, (datos.correo,))

        usuario = cursor.fetchone()

        # Verificar que exista el usuario y coincida la contraseña.
        if usuario is None:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos"
            )

        contrasena_valida, migrar_contrasena = verify_password(
            datos.contrasena, usuario["contrasena"]
        )
        if not contrasena_valida:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos"
            )

        if migrar_contrasena:
            cursor.execute(
                "UPDATE usuario SET contrasena = %s WHERE id_usuario = %s",
                (hash_password(datos.contrasena), usuario["id_usuario"]),
            )
            conn.commit()

        # Verificar que el rol seleccionado coincida con el de Neon.
        if (
            usuario["nombre_rol"].strip().casefold()
            != datos.rol.strip().casefold()
        ):
            raise HTTPException(
                status_code=403,
                detail="El rol seleccionado no corresponde a este usuario"
            )

        token, expires_in = crear_token_acceso(usuario, datos.recordar)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true",
            samesite="lax",
            max_age=expires_in,
            path="/",
        )

        # No enviar la contraseña al frontend.
        return {
            "mensaje": "Inicio de sesión exitoso",
            "token_type": "bearer",
            "expires_in": expires_in,
            "usuario": {
                "id_usuario": usuario["id_usuario"],
                "nombre_usuario": usuario["nombre_usuario"],
                "correo": usuario["correo"],
                "id_rol": usuario["id_rol"],
                "rol": usuario["nombre_rol"]
            }
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al validar las credenciales"
        )

    finally:
        conn.close()


@router.post("/logout")
def cerrar_sesion(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        path="/",
    )
    return {"mensaje": "Sesión cerrada correctamente"}