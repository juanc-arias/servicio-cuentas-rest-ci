import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Servicio REST de Consulta de Cuenta",
    description="Servicio wrapper que expone la consulta de información básica de una cuenta bancaria.",
    version="2.0.0"
)

LEGACY_CORE_URL = os.getenv("LEGACY_CORE_URL", "http://localhost:9000")


@app.get("/")
def inicio():
    return {
        "mensaje": "Servicio REST wrapper funcionando correctamente"
    }


@app.get(
    "/api/cuentas/{numero_cuenta}",
    tags=["Cuentas"],
    summary="Consultar cuenta",
    description="Consulta la información básica de una cuenta bancaria a través del core bancario legado simulado.",
    responses={
        200: {"description": "Consulta realizada correctamente"},
        404: {"description": "La cuenta no fue encontrada"},
        503: {"description": "No fue posible comunicarse con el core legado"}
    }
)
def consultar_cuenta(numero_cuenta: str):
    try:
        respuesta = httpx.get(
            f"{LEGACY_CORE_URL}/legacy/cuentas/{numero_cuenta}",
            timeout=5.0
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible comunicarse con el core bancario legado simulado"
        )

    if respuesta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"La cuenta {numero_cuenta} no fue encontrada"
        )

    if respuesta.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="El core bancario legado simulado respondió con un error inesperado"
        )

    return respuesta.json()