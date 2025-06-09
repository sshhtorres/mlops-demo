#!/bin/bash
#
# Provisionar recursos de infraestructura en Google Cloud con Terraform
#
# Uso:
#     provision.sh [COMMAND] [PROJECT_ID] [TF_OPTIONS]
#
# Comandos:
#     provision.sh  # ejecuta init-plan-apply
#     provision.sh init-plan-apply [PROJECT_ID]
#     provision.sh init [PROJECT_ID] [TF_OPTIONS]
#     provision.sh plan [TF_OPTIONS]
#     provision.sh apply [TF_OPTIONS]
#     provision.sh output [TF_OPTIONS]
#     provision.sh destroy [PROJECT_ID] [TF_OPTIONS]
#
# Ejemplos:
#     provision.sh init PROJECT_ID
#     provision.sh plan -var project_id=$PROJECT_ID -out .terraform.plan
#     provision.sh apply -auto-approve .terraform.plan
#

set -e

BASE_DIR="$(realpath $(dirname $0))"
COMMAND=$1

STDERR_START="icesi: error: $(basename $0):"
TF_DIR="${BASE_DIR}/terraform"

if [[ -z "$COMMAND" ]]; then
    bash "$0" init-plan-apply
    exit 0

elif [[ "$COMMAND" == "plan" || "$COMMAND" == "apply" || "$COMMAND" == "output" ]]; then
    terraform -chdir="${TF_DIR}" "${COMMAND}" "${@:2}"
    exit 0

elif [[ "$COMMAND" == "-h" || "$COMMAND" == *"help"* ]]; then
    cat << __EOF__
Provisionar recursos de infraestructura en Google Cloud con Terraform

Uso:
    provision.sh [COMMAND] [PROJECT_ID] [TF_OPTIONS]

Comandos:
    provision.sh  # ejecuta init-plan-apply
    provision.sh init-plan-apply [PROJECT_ID]
    provision.sh init [PROJECT_ID] [TF_OPTIONS]
    provision.sh plan [TF_OPTIONS]
    provision.sh apply [TF_OPTIONS]
    provision.sh output [TF_OPTIONS]
    provision.sh destroy [PROJECT_ID] [TF_OPTIONS]

Ejemplos:
    provision.sh init PROJECT_ID
    provision.sh plan -var project_id=$PROJECT_ID -out .terraform.plan
    provision.sh apply -auto-approve .terraform.plan
__EOF__

    exit 0

fi


PROJECT_ID="${2:-$DEVSHELL_PROJECT_ID}"
GCLOUD_PROJECT_ID="$(gcloud info --format='value(config.project)')"
if [[ -z "${PROJECT_ID}" ]]; then
    PROJECT_ID=$GCLOUD_PROJECT_ID
elif [[ "${GCLOUD_PROJECT_ID}" != "${PROJECT_ID}" ]]; then
    gcloud config set project $PROJECT_ID
fi


if [[ "$COMMAND" == "init-plan-apply" ]]; then
    bash "$0" init $PROJECT_ID 
    bash "$0" plan -var project_id=$PROJECT_ID -out .terraform.plan
    bash "$0" apply -auto-approve .terraform.plan
    exiit 0

elif [[ "$COMMAND" == "init" ]]; then
    TF_STATES_BUCKET_NAME=tfstates-${PROJECT_ID}
    terraform -chdir="${TF_DIR}" init \
        -backend-config="bucket=${TF_STATES_BUCKET_NAME}" \
        -backend-config="prefix=icesi-mlops-2025a" \
        "${@:3}"

    exit 0

elif [[ "$COMMAND" == "destroy" ]]; then
    terraform -chdir="${TF_DIR}" destroy -var project_id="$PROJECT_ID" "${@:3}"
    exit 0

else
    echo "${STDERR_START} comando no soportado: ${COMMAND}"
    exit 1

fi
