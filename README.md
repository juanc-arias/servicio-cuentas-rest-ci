# Servicio de Cuentas REST - Integración Continua

Proyecto académico desarrollado para el curso de **Integración Continua**.  
El proyecto toma como base un microservicio REST de consulta de cuentas bancarias y lo adapta a una arquitectura contenerizada usando **Docker** y **Docker Compose**.

## Contexto del proyecto

El caso de estudio representa una situación típica en entidades financieras que cuentan con un core bancario legado. Estos sistemas suelen ser rígidos, altamente acoplados y difíciles de exponer directamente hacia nuevos canales digitales.

Para representar una solución gradual, se aplica el patrón arquitectónico **Legacy Wrapper**, que permite exponer funcionalidades de un sistema legado mediante una interfaz moderna, sin modificar directamente el núcleo del sistema heredado.

En esta versión del proyecto, el sistema fue separado en dos servicios independientes:

1. **Wrapper REST**: servicio moderno que recibe las solicitudes del cliente.
2. **Core bancario legado simulado**: servicio interno que contiene datos mockeados y simula la funcionalidad heredada.

Ambos servicios se ejecutan en contenedores Docker independientes y se comunican entre sí mediante HTTP dentro de una red administrada por Docker Compose.

---

## Arquitectura general

```text
Cliente / Navegador / Postman
        ↓
Contenedor 1: wrapper-api-service
FastAPI - Servicio REST moderno
        ↓ HTTP interno
Contenedor 2: legacy-core-service
FastAPI - Core bancario legado simulado
```

---

## Tecnologías utilizadas

- Python 3.13
- FastAPI
- Uvicorn
- HTTPX
- Docker
- Docker Compose
- Git
- GitHub

---

## Estructura del proyecto

```text
servicio-cuentas-rest-ci/
│
├── wrapper_service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── legacy_core_service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Descripción de los servicios

### 1. `wrapper_service`

Servicio REST moderno construido con FastAPI.  
Su responsabilidad es recibir las solicitudes del cliente, consultar internamente al core bancario legado simulado y devolver la respuesta en formato JSON.

Endpoint principal:

```text
GET /api/cuentas/{numero_cuenta}
```

Ejemplo:

```text
http://localhost:8000/api/cuentas/123456
```

Documentación automática:

```text
http://localhost:8000/docs
```

---

### 2. `legacy_core_service`

Servicio interno construido con FastAPI que simula el comportamiento de un core bancario legado.

Contiene datos mockeados de cuentas bancarias y expone un endpoint interno para ser consultado por el servicio wrapper.

Endpoint principal:

```text
GET /legacy/cuentas/{numero_cuenta}
```

Ejemplo:

```text
http://localhost:9000/legacy/cuentas/123456
```

---

## Comunicación entre contenedores

La comunicación entre los servicios se realiza mediante Docker Compose.

El servicio `wrapper-api` se comunica con el servicio `legacy-core` usando la variable de entorno:

```text
LEGACY_CORE_URL=http://legacy-core:9000
```

Dentro de Docker Compose, los servicios pueden comunicarse usando el nombre definido en el archivo `docker-compose.yml`.

Por esta razón, el wrapper no consulta a `localhost`, sino al nombre interno del servicio:

```text
http://legacy-core:9000
```

Esto permite que el contenedor `wrapper-api-service` consulte internamente al contenedor `legacy-core-service`.

---

## Ejecución del proyecto con Docker Compose

Desde la raíz del proyecto, ejecutar:

```bash
docker compose up --build
```

Este comando construye las imágenes y levanta los dos contenedores definidos en `docker-compose.yml`.

---

## Validación de contenedores activos

En otra terminal, ejecutar:

```bash
docker ps
```

Se deben observar dos contenedores en ejecución:

```text
legacy-core-service
wrapper-api-service
```

---

## Pruebas funcionales

### Consulta directa al core bancario legado simulado

```text
http://localhost:9000/legacy/cuentas/123456
```

Respuesta esperada:

```json
{
  "cuenta": "123456",
  "titular": "Carlos Gómez",
  "saldo": 4250000,
  "estado": "activa",
  "moneda": "COP"
}
```

---

### Consulta al servicio wrapper

```text
http://localhost:8000/api/cuentas/123456
```

Respuesta esperada:

```json
{
  "cuenta": "123456",
  "titular": "Carlos Gómez",
  "saldo": 4250000,
  "estado": "activa",
  "moneda": "COP"
}
```

Esta prueba evidencia que el contenedor `wrapper-api-service` se comunica correctamente con el contenedor `legacy-core-service`.

---

### Consulta de cuenta inexistente

```text
http://localhost:8000/api/cuentas/999999
```

Respuesta esperada:

```json
{
  "detail": "La cuenta 999999 no fue encontrada"
}
```

---

## Detener los contenedores

Para detener y eliminar los contenedores creados por Docker Compose:

```bash
docker compose down
```

---

## Comandos útiles

Construir y levantar los servicios:

```bash
docker compose up --build
```

Levantar los servicios en segundo plano:

```bash
docker compose up -d --build
```

Ver contenedores activos:

```bash
docker ps
```

Ver logs de los servicios:

```bash
docker compose logs
```

Detener los servicios:

```bash
docker compose down
```

---

## Objetivo académico

El objetivo de esta versión del proyecto es demostrar el uso de Docker para construir dos contenedores comunicados entre sí, como parte de la primera entrega del curso de Integración Continua.

La solución permite evidenciar:

- Separación de responsabilidades entre servicios.
- Construcción de imágenes Docker.
- Ejecución de contenedores independientes.
- Comunicación interna entre contenedores.
- Uso de Docker Compose para orquestar servicios.
- Aplicación conceptual del patrón Legacy Wrapper en un escenario bancario simulado.

---

## Autor

Proyecto académico desarrollado para el curso de Integración Continua.