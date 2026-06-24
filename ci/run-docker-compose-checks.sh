#!/usr/bin/env bash

set -euo pipefail

compose() {
  if docker compose version >/dev/null 2>&1; then
    docker compose "$@"
  elif command -v docker-compose >/dev/null 2>&1; then
    docker-compose "$@"
  else
    echo "No se encontró Docker Compose."
    exit 1
  fi
}

cleanup() {
  echo "Limpiando ambiente..."
  compose down --remove-orphans || true
}

trap cleanup EXIT

echo "Validando configuración de Docker Compose..."
compose config

echo "Construyendo imágenes..."
compose build

echo "Levantando servicios..."
compose up -d

echo "Estado de los servicios..."
compose ps

echo "Esperando disponibilidad del wrapper..."
for intento in $(seq 1 30); do
  if python ci/test_integration.py --health-only; then
    echo "Servicios disponibles."
    break
  fi

  echo "Intento ${intento}/30: servicios aún no disponibles."
  sleep 2

  if [ "$intento" -eq 30 ]; then
    echo "Los servicios no estuvieron disponibles dentro del tiempo esperado."
    compose logs
    exit 1
  fi
done

echo "Ejecutando pruebas de integración..."
python ci/test_integration.py