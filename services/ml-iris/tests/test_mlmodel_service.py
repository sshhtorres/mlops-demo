import logging
import os
import tempfile
from unittest.mock import patch, MagicMock

import numpy as np
import onnxruntime as ort
from onnxruntime import InferenceSession
import pytest

from entities import PredictRequest, PredictResponse, PredictResponseMetadata
from mlmodel_service import MLModelService, CATEGORIES


class DummyInferenceSession:
    def __init__(self, preds=None):
        self._inputs = [MagicMock(name='input', spec=['name'])]
        self._inputs[0].name = 'input_0'
        self._output = np.array([]) if preds is None else np.array([preds])


    def get_inputs(self):
        return self._inputs


    def run(self, _, inputs):
        return self._output


class TestMLModelService:
    def setup_method(self):
        self.service = MLModelService()


    def test_is_model_loaded_false(self):
        assert not self.service.is_model_loaded()


    def test_is_model_loaded_true(self):
        self.service.sess = DummyInferenceSession()
        assert self.service.is_model_loaded()


    def test_load_model_file_not_exists(self):
        with pytest.raises(RuntimeError):
            self.service.load_model("non_existent.onnx")


    @patch("mlmodel_service.InferenceSession")
    @patch("mlmodel_service.ort.get_available_providers", return_value=["CPUExecutionProvider"])
    def test_load_model_success(self, mock_providers, mock_infsess):
        with tempfile.NamedTemporaryFile(suffix=".onnx") as tmp:
            mock_infsess.return_value = DummyInferenceSession()
            self.service.load_model(tmp.name)
            assert self.service.sess is not None
            assert self.service.model_id == os.path.basename(tmp.name)


    def test_predict_raises_if_not_loaded(self):
        req = PredictRequest(instances=[[5.1, 3.5, 1.4, 0.2]], config=None)
        with pytest.raises(RuntimeError):
            self.service.predict(req)


    def test_predict_success(self):
        # prueba unitaria usando un mock, no se utiliza el modelo
        instances = [
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ]
        preds = [0, 1, 2]

        self.service.model_id = "dummy.onnx"
        self.service.sess = DummyInferenceSession(preds)

        req = PredictRequest(instances=instances, config=None)
        resp = self.service.predict(req)

        assert isinstance(resp, PredictResponse)
        assert resp.metadata.categories == CATEGORIES
        assert resp.model_id == "dummy.onnx"
        assert resp.predictions == preds


    def test_input_data_from_request_instances(self):
        req = PredictRequest(instances=[[1, 2, 3, 4]], config=None)
        arr = MLModelService.input_data_from_request(req)
        assert isinstance(arr, np.ndarray)
        assert arr.shape == (1, 4)
        assert arr.dtype == np.float32


    def test_input_data_from_request_config_file(self):
        arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=np.float32)
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            np.savetxt(tmp, arr, delimiter=",")
            tmp.flush()
            req = PredictRequest(instances=None, config={"csv_file_uri": tmp.name, "delimeter": ","})
            loaded = MLModelService.input_data_from_request(req)
            assert np.allclose(loaded, arr)
        
        os.remove(tmp.name)


    def test_input_data_from_request_raises(self):
        req = PredictRequest(instances=None, config=None)
        with pytest.raises(ValueError):
            MLModelService.input_data_from_request(req)
