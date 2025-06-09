import logging
import os
from urllib.parse import urlparse

from google.cloud import storage
import httpx

from config import MLMODELS_DIR


logger = logging.getLogger(__name__)


def download_model_from_http(model_uri: str, models_dir: str = MLMODELS_DIR) -> str:
    filename = os.path.basename(urlparse(model_uri).path)
    filepath = os.path.join(models_dir, filename)

    os.makedirs(models_dir, exist_ok=True)
    try:
        with httpx.stream("GET", model_uri) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        logger.info(f'Model downloaded from "{model_uri}" to "{filepath}"')
    except Exception as e:
        logger.error(f"Failed to download model from {model_uri}: {e}")
        raise

    return filepath


def download_model_from_gcs(model_uri: str, models_dir: str = MLMODELS_DIR) -> str:
    parsed = urlparse(model_uri)
    if parsed.scheme != "gs":
        raise ValueError("model_uri must start with gs://")

    bucket_name = parsed.netloc
    blob_path = parsed.path.lstrip("/")
    filename = os.path.basename(blob_path)
    filepath = os.path.join(models_dir, filename)

    os.makedirs(models_dir, exist_ok=True)
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.download_to_filename(filepath)
        logger.info(f'Model downloaded from "{model_uri}" to "{filepath}"')
    except Exception as e:
        logger.error(f"Failed to download model from {model_uri}: {e}")
        raise

    return filepath
