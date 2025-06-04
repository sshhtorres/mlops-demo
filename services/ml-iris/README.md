# Servicio ML - Iris

Servicio ML para clasificar la especie de una flor según el conjunto de datos de referencia: Iris dataset: https://archive.ics.uci.edu/dataset/53/iris

Contenido:
- [Endpoints](#endpoints)
- [Ejecución](#ejecución)
- [Pruebas](#pruebas)
- [Apéndice 1: acceso a objetos de Google Cloud Storage](#apéndice-1-acceso-a-objetos-en-google-cloud-storage)


# Endpoints

El servicio soporta los siguientes endpoints y métodos HTTP:
```
GET /_health

GET /_ready

GET /docs

POST /predict
Content-Type: application/json
{"instances": [[1, 2, 3, 4], [1, 2, 3, 4]]}

POST /predict
Content-Type: application/json
{"config": {"csv_file_uri": "FILE_URI" }}

POST /predict
Content-Type: application/json
{"config": {"csv_file_uri": "FILE_URI", "delimeter": ","}}
```

En [openapi.json](openapi.json) se presenta la especificación OpenAPI del servicio.

En [src/entities.py](src/entities.py) se encuentran los modelos de solicitud-respuesta para el endpoint `/predict`.


# Ejecución

**Ejecución en local utilizando Docker:**

1. Definir la variable MLMODEL_URI con la ruta del archivo del modelo ONNX:
    ```sh
    # modelo en Google Cloud Storage
    MLMODEL_URI=https://storage.googleapis.com/BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx

    # modelo en Google Cloud Storage con acceso privado requiere credenciales (ver apéndice 1)
    MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx
    
    # modelo local a través de servidor de archivos en el directorio de modelos
    # python -m http.server 6060
    # python3 -m http.server 6060

    # el DNS del contenedor apunta `host.docker.internal` al localhost del host de Docker
    MLMODEL_URI=http://host.docker.internal:6060/iris_logreg_v12.onnx
    ```

2. Construir y ejecutar imagen del contenedor:
    ```sh
    # construir imagen
    docker build --target=service -t ml-iris .

    # ejecutar contenedor en puerto 5000
    docker run --rm --name ml-iris -e "MLMODEL_URI=${MLMODEL_URI}" -p 5000:80 ml-iris
    ```

3. Solicitar predicciones declarando instancias:
    ```sh
    INSTANCES='[[6.1, 2.8, 4.7, 1.2], [5.7, 3.8, 1.7, 0.3]]'
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": ${INSTANCES} }" \
        localhost:5000/predict
    ```

4. Solicitar predicciones referenciando archivo:
    ```sh
    # levantar servidor de archivos en el directorio local de datos
    # python -m http.server 7070
    # python3 -m http.server 7070

    # el DNS del contenedor apunta `host.docker.internal` al localhost del host de Docker
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d '{"config": {"csv_file_uri": "http://host.docker.internal:7070/iris_X_test.csv"}}' \
        localhost:5000/predict
    ```

**Ejecución en local utilizando ambiente virtual:**
1. Configurar ambiente:
    ```sh
    # Unix 
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Windows (Git-Bash)
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt

    # Windows (Power-Shell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2. Definición de variables de ambiente:
    ```sh
    MLMODELS_DIR=

    # modelo local
    MLMODEL_URI="${MLMODELS_DIR}/iris_logreg_v12.onnx"

    # modelo en Google Cloud Storage
    MLMODEL_URI=https://storage.googleapis.com/BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx

    # modelo en Google Cloud Storage con acceso privado requiere credenciales (ver apéndice 1)
    MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx
    ```

3. Iniciar servicio:
    ```sh
    # modo producción
    PYTHONPATH=src/ fastapi run src/app.py --port 8000

    # modo desarrollo
    ENVIRONMENT=development PYTHONPATH=src/ fastapi dev src/app.py --port 8000
    ```

4. Solicitar predicciones declarando instancias:
    ```sh
    INSTANCES='[[4.6, 3.6, 1.0, 0.2]]'
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": ${INSTANCES} }" \
        localhost:8000/predict
    ```

5. Solicitar predicciones referenciando archivo:
    ```sh
    DATA_TEST_FILEPATH=
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"config\": {\"csv_file_uri\": \"${DATA_TEST_FILEPATH}" }}" \
        localhost:5000/predict
    ```

# Pruebas

**Pruebas en local utilizando Docker:**
```sh
# crear imagen de pruebas
docker build --target testing -t ml-iris-testing .

# ejecutar contenedor de pruebas
docker run --rm --name ml-iris-testing ml-iris-testing
```

**Pruebas en local utilizando ambiente virtual (previamente creado):**
```sh
# instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# correr pruebas unitarias
pytest
```


# Apéndice 1: acceso a objetos en Google Cloud Storage

Se requiere asignar credenciales para acceder a objetos en Google Cloud Storage a través de la libería cliente `google-cloud-storage`.
```sh
gcloud auth application-default login
```

Ejecución en local utilizando ambiente virtual donde `google-cloud-storage` automáticamente utiliza las credenciales y lee el proyecto actual de Google Cloud:
```sh
MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx

# modo producción
PYTHONPATH=src/ fastapi run src/app.py --port 8000
```

Ejecución con Docker requiere mapear las credenciales al contenedor y definir el proyecto actual de Google Cloud:
- en Unix (Linux, macOS):
    ```sh
    GOOGLE_CLOUD_PROJECT=
    MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx

    CREDENTIALS="${HOME}/.config/gcloud/application_default_credentials.json"

    docker run --rm --name ml-iris \
        -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
        -e "GOOGLE_APPLICATION_CREDENTIALS=/application_default_credentials.json" \
        -e "MLMODEL_URI=${MLMODEL_URI}" \
        -p 5000:80 \
        -v "${CREDENTIALS}:/application_default_credentials.json:ro" \
        ml-iris
    ```

- en Windows (PowerShell):
    ```powershell
    $GOOGLE_CLOUD_PROJECT =
    $MLModelUri = "gs://BUCKET_NAME/PATH/TO/MODEL/iris_logreg_v12.onnx"

    $Credentials = "$env:APPDATA\gcloud\application_default_credentials.json"
    
    docker run --rm --name ml-iris `
        -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" `
        -e "GOOGLE_APPLICATION_CREDENTIALS=/application_default_credentials.json" `
        -e "MLMODEL_URI=${MLModelUri}" `
        -p 5000:80 `
        -v "${CREDENTIALS}:/application_default_credentials.json:ro" `
        ml-iris
    ```

Nota: mapear volúmenes de Docker desde Windows Git-Bash puede resultar en errores de rutas apuntando a "C:/Program Files/Git/", por lo que es preferible utilizar PowerShell.
