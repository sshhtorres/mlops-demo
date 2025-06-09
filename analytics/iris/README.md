# Modelo Iris - clasificación de especie

**Desarrollo de modelo y datos en local:**

1. Configurar ambiente virtual local:
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

2. Desarrollo de modelo y escritura de modelo:
```sh
python -m scripts.fit_write_model --name iris_logreg_v1.onnx --dir .models/
```

3. Guardar datos de prueba:
```sh
python -m scripts.write_test_data --dir .data/
```


**Carga de modelo y datos a Google Cloud Storage:**
1. Configurar autenticación de Google Cloud:
```sh
# Opción 1: si está utilizando Cloud Shell ya está autenticado

# Opción 2: configurar gcloud
gcloud config set project PROJECT_ID
gcloud auth login application-default

# Opción 3: Definir GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS=
```

2. Carga de modelo y datos a Google Cloud Storage:
```sh
# cargar modelo
python -m scripts.upload_file_to_gcs --name iris_logreg_v1.onnx --dir .models/ --gcs gs://BUCKET_NAME/models

# cargar datos de prueba
python -m scripts.upload_test_data_to_gcs --dir .data/ --gcs gs://BUCKET_NAME/data
```
