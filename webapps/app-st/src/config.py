import os

import streamlit as st

from entities import AppConfig, MLServiceConfig


@st.cache_data
def get_app_config() -> AppConfig:
    mlservices = {
        "iris": MLServiceConfig(
            id="iris",
            request_body_samples=[
                '{"instances": [[1, 2, 3, 4], [1, 2, 3, 4]]}'
            ],
            service_url=os.environ.get("ML_IRIS_SERVICE_URL")
        ),
        "mnist": MLServiceConfig(id="mnist", service_url=os.environ.get("ML_MNIST_SERVICE_URL")),
    }
    return AppConfig(mlservices=mlservices)
