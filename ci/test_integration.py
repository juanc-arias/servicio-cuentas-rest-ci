import argparse
import json
import os
import sys
import urllib.request
from urllib.error import HTTPError, URLError


BASE_URL = os.getenv("CI_BASE_URL", "http://localhost:8000")


def get_json(path: str):
    url = f"{BASE_URL}{path}"
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_success_case() -> None:
    data = get_json("/api/cuentas/123456")

    assert data["cuenta"] == "123456"
    assert data["estado"] == "activa"
    assert data["moneda"] == "COP"

    print("Prueba de integración exitosa para cuenta 123456:")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def validate_not_found_case() -> None:
    url = f"{BASE_URL}/api/cuentas/999999"

    try:
        urllib.request.urlopen(url, timeout=5)
        raise AssertionError("Se esperaba una respuesta HTTP 404.")
    except HTTPError as error:
        assert error.code == 404
        response = json.loads(error.read().decode("utf-8"))
        assert response["detail"] == "La cuenta 999999 no fue encontrada"

        print("Prueba de error 404 exitosa:")
        print(json.dumps(response, ensure_ascii=False, indent=2))


def health_check() -> None:
    get_json("/api/cuentas/123456")
    print("Servicio disponible.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--health-only", action="store_true")
    args = parser.parse_args()

    try:
        if args.health_only:
            health_check()
        else:
            validate_success_case()
            validate_not_found_case()

        return 0

    except (AssertionError, HTTPError, URLError, TimeoutError) as error:
        print(f"Error en las pruebas de integración: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())