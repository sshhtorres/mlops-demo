# Modelo MNIST - clasificación de imágenes de dígitos escritos

Conjunto de datos de referencia MNIST: https://en.wikipedia.org/wiki/MNIST_database

**Desarrollo de modelo y datos en local:**

1. Configurar ambiente virtual local con `uv` ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)):
    ```sh
    # multiplataforma 
    uv sync
    ```

2. Desarrollo y escritura de modelo:
    ```sh
    uv run modelo.py
    ```


**Carga de modelo a Google Cloud Storage:**
1. Configurar autenticación de Google Cloud:
    ```sh
    # Opción 1: si está utilizando Cloud Shell ya está autenticado

    # Opción 2: configurar gcloud
    gcloud config set project PROJECT_ID
    gcloud auth login application-default

    # Opción 3: Definir GOOGLE_APPLICATION_CREDENTIALS
    export GOOGLE_APPLICATION_CREDENTIALS=
    ```

2. Carga de modelo a Google Cloud Storage:
    ```sh
    BUCKET_NAME=
    gsutil cp .models/mnist_v1.onnx "gs://${BUCKET_NAME}/models/mnist_v1.onnx"
    ```
