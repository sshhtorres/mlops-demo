import base64
import io
import json

import httpx
import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

from components.custom import render_custom_component
from utils.mlservices import request_mlservice


SERVICE_ID = "mnist"


def render():
    st.subheader("Dibuje un número")

    drawing_json = render_custom_component("canvas", key="my_unique_key")
    if not drawing_json:
        return

    try:
        drawing = json.loads(drawing_json)
    except json.JSONDecodeError:
        st.error("icesi: error decoding drawing JSON value from canvas custom component")
        return

    decoded = base64.b64decode(drawing["image_base64"])
    image_resized = Image.open(io.BytesIO(decoded)).convert("L").resize((28, 28))

    buffered = io.BytesIO()
    image_resized.save(buffered, format="PNG")
    image_resized_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    request_body = {
        "instances": [image_resized_base64]
    }
    response_body = ""
    try:
        response_body = request_mlservice(json=request_body, timeout=10)
    except json.JSONDecodeError:
        st.error("Invalid JSON in response body.")
    except httpx.RequestError as e:
        st.error(f"HTTP request failed: {e}")

    if response_body == "":
        return

    st.subheader("Respuesta JSON")
    st.json(response_body)
    st.image(image_resized, caption="Imagen enviada al servicio de predicción", width=150)
