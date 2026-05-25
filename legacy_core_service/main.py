from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Core Bancario Legado Simulado",
    description="Servicio interno que simula la consulta de cuentas desde un core bancario legado.",
    version="1.0.0"
)

cuentas_mock = {
    "123456": {
        "cuenta": "123456",
        "titular": "Carlos Gómez",
        "saldo": 4250000,
        "estado": "activa",
        "moneda": "COP"
    },
    "789012": {
        "cuenta": "789012",
        "titular": "Laura Martínez",
        "saldo": 980000,
        "estado": "bloqueada",
        "moneda": "COP"
    }
}


@app.get("/")
def inicio():
    return {
        "mensaje": "Core bancario legado simulado funcionando correctamente"
    }


@app.get("/legacy/cuentas/{numero_cuenta}")
def consultar_cuenta_legacy(numero_cuenta: str):
    cuenta = cuentas_mock.get(numero_cuenta)

    if cuenta is None:
        raise HTTPException(
            status_code=404,
            detail=f"La cuenta {numero_cuenta} no fue encontrada en el core legado"
        )

    return cuenta