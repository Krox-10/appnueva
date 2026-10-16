from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
from pydantic import BaseModel
from app.core.database import Database

class LoginRequest(BaseModel):
    correo: str
    contrasena: str
    rol: str

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"]
)

repo = UsuarioRepository()


@router.get("/")
def listar_usuarios():
    return repo.obtener_todos()


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return repo.obtener_por_id(usuario_id)


@router.post("/")
def crear_usuario(usuario: Usuario):
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
    repo.actualizar(usuario_id, usuario)

    return {
        "mensaje": "Usuario actualizado correctamente"
    }

@router.post("/login")
def iniciar_sesion(datos: LoginRequest):
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
        if (
            usuario is None
            or usuario["contrasena"] != datos.contrasena
        ):
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos"
            )

        # Verificar que el rol seleccionado coincida con el de Neon.
        if (
            usuario["nombre_rol"].strip().casefold()
            != datos.rol.strip().casefold()
        ):
            raise HTTPException(
                status_code=403,
                detail="El rol seleccionado no corresponde a este usuario"
            )

        # No enviar la contraseña al frontend.
        return {
            "mensaje": "Inicio de sesión exitoso",
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