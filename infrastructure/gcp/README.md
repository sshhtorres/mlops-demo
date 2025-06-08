# Infraestructura en Google Cloud

Configuración y provisionamiento de recursos en un proyecto de Google Cloud con facturación habilitada.

# Configuración y provisionamiento

Configurar autenticación de Google Cloud:
```sh
# Opción 1: si está utilizando Cloud Shell ya está autenticado

# Opción 2: si está utilizando otra terminal
gcloud config set project PROJECT_ID
gcloud auth login
gcloud auth application-default login
```

Configurar y provisionar proyecto actual de Google Cloud con recursos en `region=us-central1`:
```sh
bash setup.sh
bash provision.sh
```

Opcionalmente, algunas indicaciones avanzadas para configuración y provisionamiento:
```sh
# configurar y provisionar un proyecto Google Cloud con recursos en `region=us-central1`
bash setup.sh PROJECT_ID
bash provision.sh PROJECT_ID

# provisionamiento de un proyecto Google Cloud con recursos en REGION
bash setup.sh PROJECT_ID REGION
bash provision.sh PROJECT_ID REGION

# provisionamiento paso a paso de un proyecto en Google Cloud
bash provision.sh init $PROJECT_ID
bash provision.sh plan -var project_id=$PROJECT_ID -var region=$REGION -out .terraform.plan
bash provision.sh apply -auto-approve .terraform.plan
bash provision.sh destroy $PROJECT_ID
```

# Consideraciones

- El estado de Terraform es guardado en el bucket `TF_STATES_BUCKET_NAME=tfstates-${PROJECT_ID}` definido en [setup.sh](./setup.sh) y [provision.sh](./provision.sh)
