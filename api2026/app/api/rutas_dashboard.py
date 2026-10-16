from fastapi import APIRouter, HTTPException

from app.core.database import Database


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard de Inicio"]
)

LIMITE_ITEMS = 3


@router.get("/resumen")
def obtener_resumen():
    """
    Devuelve los datos que se muestran en la página de inicio:
    - Totales (miembros, semilleros activos, investigaciones y eventos).
    - Los 3 semilleros con más miembros y más proyectos.
    - Los 3 eventos (reuniones) más nuevos.
    """
    db = Database()
    conn = db.get_connection()

    if conn is None:
        raise HTTPException(
            status_code=500,
            detail="No fue posible conectar con la base de datos"
        )

    try:
        cursor = conn.cursor()

        # ---------- TOTALES ----------
        cursor.execute("""
            SELECT
                (SELECT COUNT(*)
                   FROM usuario
                  WHERE estado = TRUE
                    AND id_semillero IS NOT NULL) AS miembros,
                (SELECT COUNT(*)
                   FROM semillero
                  WHERE estado = TRUE)            AS semilleros,
                (SELECT COUNT(*)
                   FROM investigacion
                  WHERE estado = TRUE)            AS investigaciones,
                (SELECT COUNT(*)
                   FROM reunion
                  WHERE estado = TRUE)            AS eventos;
        """)
        totales = cursor.fetchone()

        # ---------- SEMILLEROS (más miembros y más proyectos) ----------
        cursor.execute("""
            SELECT
                s.id_semillero,
                s.nombre,
                (SELECT COUNT(*)
                   FROM usuario u
                  WHERE u.id_semillero = s.id_semillero
                    AND u.estado = TRUE)          AS miembros,
                (SELECT COUNT(*)
                   FROM investigacion i
                  WHERE i.id_semillero = s.id_semillero
                    AND i.estado = TRUE)          AS proyectos
            FROM semillero s
            WHERE s.estado = TRUE
            ORDER BY miembros DESC, proyectos DESC, s.nombre ASC
            LIMIT %s;
        """, (LIMITE_ITEMS,))
        semilleros = cursor.fetchall()

        # ---------- EVENTOS (los más nuevos primero) ----------
        cursor.execute("""
            SELECT
                r.id_reunion,
                r.tema,
                r.fecha,
                r.hora_inicio,
                s.nombre AS semillero
            FROM reunion r
            LEFT JOIN semillero s ON s.id_semillero = r.id_semillero
            WHERE r.estado = TRUE
            ORDER BY r.fecha DESC, r.hora_inicio DESC
            LIMIT %s;
        """, (LIMITE_ITEMS,))
        eventos = cursor.fetchall()

        return {
            "totales": {
                "miembros": totales["miembros"],
                "semilleros": totales["semilleros"],
                "investigaciones": totales["investigaciones"],
                "eventos": totales["eventos"]
            },
            "semilleros": [
                {
                    "id_semillero": s["id_semillero"],
                    "nombre": s["nombre"],
                    "miembros": s["miembros"],
                    "proyectos": s["proyectos"]
                }
                for s in semilleros
            ],
            "eventos": [
                {
                    "id_reunion": e["id_reunion"],
                    "tema": e["tema"],
                    "fecha": e["fecha"].isoformat() if e["fecha"] else None,
                    "hora_inicio": (
                        e["hora_inicio"].strftime("%H:%M")
                        if e["hora_inicio"] else None
                    ),
                    "semillero": e["semillero"]
                }
                for e in eventos
            ]
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Error al obtener el resumen del dashboard:", error)
        raise HTTPException(
            status_code=500,
            detail="Error al obtener el resumen del inicio"
        )

    finally:
        conn.close()
