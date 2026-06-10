pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Descargando el código desde GitHub...'
                checkout scm
            }
        }

        stage('Validar Docker Compose') {
            steps {
                echo 'Validando la configuración docker-compose.yml...'
                sh 'docker compose config'
            }
        }

        stage('Construir imágenes') {
            steps {
                echo 'Construyendo las imágenes Docker...'
                sh 'docker compose build'
            }
        }

        stage('Levantar servicios') {
            steps {
                echo 'Iniciando los contenedores del proyecto...'
                sh 'docker compose up -d'
                sh 'docker compose ps'
            }
        }

        stage('Esperar disponibilidad') {
            steps {
                echo 'Esperando a que los servicios estén disponibles...'

                sh '''
                    for intento in $(seq 1 30); do
                        if docker compose exec -T wrapper-api python -c "
import urllib.request
urllib.request.urlopen(
    'http://localhost:8000/api/cuentas/123456',
    timeout=3
).read()
"; then
                            echo "Los servicios están disponibles."
                            exit 0
                        fi

                        echo "Intento ${intento}/30: servicios aún no disponibles."
                        sleep 2
                    done

                    echo "Los servicios no estuvieron disponibles dentro del tiempo esperado."
                    docker compose logs
                    exit 1
                '''
            }
        }

        stage('Prueba de integración') {
            steps {
                echo 'Validando la comunicación entre los contenedores...'

                sh '''
                    docker compose exec -T wrapper-api python -c "
import json
import urllib.request

with urllib.request.urlopen(
    'http://localhost:8000/api/cuentas/123456',
    timeout=5
) as respuesta:
    datos = json.load(respuesta)

assert datos['cuenta'] == '123456'
assert datos['estado'] == 'activa'
assert datos['moneda'] == 'COP'

print('Prueba exitosa. Respuesta recibida:')
print(json.dumps(datos, ensure_ascii=False, indent=2))
"
                '''
            }
        }

        stage('Prueba de cuenta inexistente') {
            steps {
                echo 'Validando el manejo del error 404...'

                sh '''
                    docker compose exec -T wrapper-api python -c "
import json
import urllib.request
from urllib.error import HTTPError

try:
    urllib.request.urlopen(
        'http://localhost:8000/api/cuentas/999999',
        timeout=5
    )
    raise AssertionError('Se esperaba una respuesta HTTP 404.')
except HTTPError as error:
    assert error.code == 404
    respuesta = json.loads(error.read().decode('utf-8'))
    assert respuesta['detail'] == 'La cuenta 999999 no fue encontrada'
    print('Prueba de error 404 exitosa:')
    print(json.dumps(respuesta, ensure_ascii=False, indent=2))
"
                '''
            }
        }
    }

    post {
        always {
            echo 'Deteniendo y eliminando los contenedores temporales...'
            sh 'docker compose down --remove-orphans || true'
        }

        success {
            echo 'Pipeline ejecutado correctamente.'
        }

        failure {
            echo 'El pipeline presentó errores. Revisa los logs de la ejecución.'
        }
    }
}