import logging
import os
from typing import Any

import numpy
import onnxruntime as ort
from onnxruntime import InferenceSession

from entities import PredictRequest, PredictResponse, PredictResponseMetadata
from utils import download_model_from_gcs, download_model_from_http


CATEGORIES = ['setosa', 'versicolor', 'virginica']


logger = logging.getLogger(__name__)


class MLModelService:
    model_id: str | None = None
    sess: InferenceSession | None = None


    def is_model_loaded(self) -> bool:
        return self.sess is not None


    def load_model(self, model_uri: str):    
        if model_uri.startswith("http://") or model_uri.startswith("https://"):
            filepath = download_model_from_http(model_uri)
        elif model_uri.startswith("gs://"):
            filepath = download_model_from_gcs(model_uri)
        elif model_uri.startswith("file://"):
            filepath = model_uri[7:]
        else:
            filepath = model_uri

        if not os.path.exists(filepath):
            raise RuntimeError(f"El archivo del modelo no existe: {filepath}")

        self.model_id = os.path.basename(filepath)
        try:
            self.sess = InferenceSession(filepath, providers=ort.get_available_providers())
            logger.info(f"Modelo correctamente cargado: {filepath}")
        except Exception as e:
            logger.error(f"Error al cargar el modelo desde {filepath}: {e}")
            raise RuntimeError(f"Error al cargar el modelo")


    def predict(self, request: PredictRequest) -> PredictResponse:
        if not self.is_model_loaded():
            raise RuntimeError("No se ha cargado ningún modelo para predicción")

        input_data = self.input_data_from_request(request)
        input_name = self.sess.get_inputs()[0].name
        inputs = {input_name: input_data}
        outputs = self.sess.run(None, inputs)
        preds = outputs[0]

        return PredictResponse(
            model_id=self.model_id,
            metadata=PredictResponseMetadata(categories=CATEGORIES),
            predictions=preds.tolist()
        )


    @staticmethod
    def input_data_from_request(request: PredictRequest) -> numpy.ndarray:
        if request.config is None and request.instances is None:
            raise ValueError("Se requiere al menos una instancia de entrada para la predicción")

        elif request.config is None:
            input_data = numpy.array(request.instances).astype(numpy.float32)

        else:
            csv_file_uri = request.config.csv_file_uri
            delimeter = request.config.delimeter
            input_data = numpy.loadtxt(csv_file_uri, delimiter=delimeter, dtype=numpy.float32)

        return input_data
