import os
import tempfile
from unittest import mock

import pytest

from utils import download_model_from_gcs, download_model_from_http


def test_download_model_from_http(tmp_path):
    # Mock httpx.stream to simulate a file download
    test_content = b"test model data"
    test_url = "http://example.com/model.pkl"
    filename = "model.pkl"
    models_dir = tmp_path

    class MockResponse:
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
        def raise_for_status(self): pass
        def iter_bytes(self): yield test_content

    with mock.patch("httpx.stream", return_value=MockResponse()):
        filepath = download_model_from_http(test_url, str(models_dir))
        assert os.path.exists(filepath)
        with open(filepath, "rb") as f:
            assert f.read() == test_content


def test_download_model_from_gcs(tmp_path):
    # Mock google.cloud.storage.Client and related methods
    test_content = b"gcs model data"
    test_url = "gs://bucket/model.pkl"
    filename = "model.pkl"
    models_dir = tmp_path

    mock_blob = mock.Mock()
    def download_to_filename(path):
        with open(path, "wb") as f:
            f.write(test_content)
    mock_blob.download_to_filename.side_effect = download_to_filename

    mock_bucket = mock.Mock()
    mock_bucket.blob.return_value = mock_blob

    mock_client = mock.Mock()
    mock_client.bucket.return_value = mock_bucket

    with mock.patch("google.cloud.storage.Client", return_value=mock_client):
        filepath = download_model_from_gcs(test_url, str(models_dir))
        assert os.path.exists(filepath)
        with open(filepath, "rb") as f:
            assert f.read() == test_content
