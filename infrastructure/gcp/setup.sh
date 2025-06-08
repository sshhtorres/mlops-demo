#!/bin/bash
#
# Configuración básica del proyecto de Google Cloud
#
# Uso:
#     setup.sh [PROJECT_ID] [REGION]
#
# Ejemplos:
#     setup.sh
#     setup.sh PROJECT_ID [REGION]
#

set -e

if [[ "$1" == "-h" || "$1" == *"help"* ]]; then
    cat << __EOF__
Configuración básica del proyecto de Google Cloud

Uso:
    setup.sh [PROJECT_ID] [REGION]

Ejemplos:
    setup.sh
    setup.sh PROJECT_ID [REGION]
__EOF__

    exit 0
fi


BASE_DIR="$(realpath $(dirname $0))"

SCRIPTS_DIR="${BASE_DIR}/scripts"
STDOUT_START="icesi:"
STDERR_START="icesi: error: $(basename $0):"

PROJECT_ID="${1:-$DEVSHELL_PROJECT_ID}"
REGION="${2:-us-central1}"

GCLOUD_PROJECT_ID="$(gcloud info --format='value(config.project)')"
if [[ -z "${PROJECT_ID}" ]]; then
    PROJECT_ID=$GCLOUD_PROJECT_ID
elif [[ "${GCLOUD_PROJECT_ID}" != "${PROJECT_ID}" ]]; then
    gcloud config set project $PROJECT_ID
fi

TF_STATES_BUCKET_NAME=tfstates-${PROJECT_ID}

echo "${STDOUT_START} $(basename $0) $PROJECT_ID $REGION"

echo "${STDOUT_START} habilitando APIs de Google Cloud..."
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable serviceusage.googleapis.com
gcloud services enable storage.googleapis.com


# bucket con versionamiento habilitado para los estados de Terraform
LISTING="$(gsutil ls)"
if [[ -z "$LISTING" || -z "$(echo "${LISTING}" | grep $TF_STATES_BUCKET_NAME)" ]]; then
    BUCKET_URI=gs://${TF_STATES_BUCKET_NAME}
    echo "${STDOUT_START} creando bucket de estados de Terraform \"${BUCKET_URI}\" en la región \"${REGION}\"..."
    gsutil mb -l "${REGION}" "${BUCKET_URI}"
    gsutil versioning set on "${BUCKET_URI}"
    gsutil label ch -l type:project "${BUCKET_URI}"
else
    echo "${STDOUT_START} se encontró bucket de estados de Terraform: \"${TF_STATES_BUCKET_NAME}\""
fi
