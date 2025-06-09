import base64
import io
import logging
import os

import numpy as np
import onnxruntime as ort
import PIL
import torchvision.transforms as transforms

from entities import PredictRequest, PredictResponse
from utils import download_model_from_gcs, download_model_from_http


logger = logging.getLogger(__name__)


class ModelService:
    model_id: str | None = None
    session: ort.InferenceSession = None


    def is_model_loaded(self) -> bool:
        return self.session is not None


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
            self.session = ort.InferenceSession(filepath, providers=ort.get_available_providers())
            logger.info(f"Modelo correctamente cargado: {filepath}")
        except Exception as e:
            logger.error(f"Error al cargar el modelo desde {filepath}: {e}")
            raise RuntimeError(f"Error al cargar el modelo")


    def predict(self, request: PredictRequest):
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name

        predictions = []
        for image_base64 in request.instances:
            image_bytes = base64.b64decode(image_base64)
            image = PIL.Image.open(io.BytesIO(image_bytes))
            image_data = ModelService.preprocess_image(image)
            results = self.session.run([output_name], {input_name: image_data})
            prediction = np.argmax(results[0])
            predictions.append(prediction)

        return PredictResponse(
            model_id=self.model_id,
            predictions=predictions
        )


    @staticmethod
    def preprocess_image(image: PIL.Image.Image):
        transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((28, 28)),
            transforms.ToTensor()
        ])
        image_data = transform(image).unsqueeze(0).numpy().astype(np.float32)
        return image_data
