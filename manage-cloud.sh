#!/bin/bash

set -e

ROOT_DIR="$(realpath $(dirname "$0"))"

COMMAND="$1"
PROJECT_ID="$2"
REGION="$3"

if [[ -z "$COMMAND" || "$COMMAND" == "-h" || "$COMMAND" == *"help"* ]]; then
    cat << __EOF__

__EOF__
    exit 0

fi

echo "icesi: ${@:0}"
STDOUT_START="icesi: $(basename $0):"
STDERR_START="icesi: error: $(basename $0):"

if [[ "$COMMAND" == "build-deploy" ]]; then
    bash "$0" build-models
    bash "$0" deploy
    exit 0

elif [[ "$COMMAND" == "setup-provision" ]]; then
    # bash "$0" setup-provision-gcp
    bash "$0" setup-github-actions
    exit 0

elif [[ "$COMMAND" == "setup-provision-gcp" ]]; then
    bash "${ROOT_DIR}/infrastructure/gcp/setup.sh"
    bash "${ROOT_DIR}/infrastructure/gcp/provision.sh"
    exit 0

fi

# definir variables comunes dependientes del estado de Terraform
TERRAFORM_OUTPUT="$(bash "${ROOT_DIR}/infrastructure/gcp/provision.sh" output -json)"
GITHUB_REPO="$(jq -r '.github_repo.value' <<< "${TERRAFORM_OUTPUT}")"

if [[ -z "$GITHUB_REPO" ]]; then
    echo "${STDERR_START} GITHUB_REPO sin definir" >&2
    exit 1
fi
echo "${STDOUT_START} GITHUB_REPO=$GITHUB_REPO"

if [[ "$COMMAND" == "build-models" ]]; then
    echo "missing implementation :)"

    # gh variable get GCS_DATA_DEST --repo "${GITHUB_REPO}"
    # gh variable get GCS_MODELS_DEST --repo "${GITHUB_REPO}"

    # ML_IRIS_MODEL_URI_DEV=gs://${GCS_MODELS_DEST}/model_iris.onnx
    # ML_IRIS_MODEL_URI_PROD=gs://${GCS_MODELS_DEST}/model_iris.onnx

    exit 0

elif [[ "$COMMAND" == "deploy" ]]; then
    service=plays/ml-iris
    deploy_env=dev

    # gh workflow run .github/workflows/playground.yaml \
    #     -f model_uri=model_ab.onnx \
    #     -f service_release=custom_service_release \
    #     --ref "$service/$deploy_env" \
    #     --repo $GITHUB_REPO

    # gh workflow run .github/workflows/deploy.yaml \
    #     -f model_uri=custom_model_ab.onnx \
    #     -f service_release=custom_release \
    #     --ref "$service" \
    #     --repo $GITHUB_REPO

    # for service in services/*; do
    #   for deploy_env in dev prod; do
    #       gh workflow run .github/workflows/deploy.yaml --ref "$service/$deploy_env" --repo $GITHUB_REPO
    #   done
    # done

elif [[ "$COMMAND" == "deploy-model" ]]; then
    
    # PENDIENTE
    #
    # gh variable set ML_IRIS_MODEL_URI_DEV --body VALUE
    # gh variable set ML_IRIS_MODEL_URI_PROD --body VALUE

    # gh variable set ML_MNIST_MODEL_URI_DEV --body VALUE
    # gh variable set ML_MNIST_MODEL_URI_PROD --body VALUE

    # gh variable set ML_IRIS_SERVICE_URL_DEV --body VALUE
    # gh variable set ML_MNIST_SERVICE_URL_DEV --body VALUE
    


elif [[ "$COMMAND" == "setup-github-actions" ]]; then
    GITHUB_ENV_VARIABLES_FILE="$(mktemp)"
    GSC_LAKE_BUCKET_NAME="$(jq -r '.lake_storage_bucket_name.value' <<< "${TERRAFORM_OUTPUT}")"

    cat << __EOF__ > "${GITHUB_ENV_VARIABLES_FILE}"
AR_HOST=$(jq -r '.services_artifact_registry_docker_repo.value.host' <<< "${TERRAFORM_OUTPUT}")
AR_REPO_URL=$(jq -r '.services_artifact_registry_docker_repo.value.url' <<< "${TERRAFORM_OUTPUT}")
GCS_DATA_DEST="gs://${GSC_LAKE_BUCKET_NAME}/data"
GCS_MODELS_DEST="gs://${GSC_LAKE_BUCKET_NAME}/models"
PROJECT_ID=$(jq -r '.project_id.value' <<< "${TERRAFORM_OUTPUT}")
REGION=$(jq -r '.region.value' <<< "${TERRAFORM_OUTPUT}")
SERVICE_ACCOUNT_EMAIL=$(jq -r '.github_actions.value.service_account' <<< "${TERRAFORM_OUTPUT}")
WORKLOAD_IDENTITY_PROVIDER=$(jq -r '.github_actions.value.workload_identity_pool_provider' <<< "${TERRAFORM_OUTPUT}")
__EOF__

    gh variable set --env-file "${GITHUB_ENV_VARIABLES_FILE}" --repo "${GITHUB_REPO}"
    rm -f "${GITHUB_ENV_VARIABLES_FILE}"

    exit 0

else
    echo "${STDERR_START} comando no soportado: ${COMMAND}"
    exit 1
fi
