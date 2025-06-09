import json

import httpx
import streamlit as st

from utils.mlservices import get_mlservice_config, request_mlservice


SERVICE_ID = "iris"


def render():   
    svc = get_mlservice_config(SERVICE_ID)
    if len(svc.request_body_samples) == 0:
        value = "{}"
    else:
        value = svc.request_body_samples[0]

    st.subheader("Solicitud JSON")
    request_body = st.text_area("Defina su solicitud JSON:", height=200, value=value)

    response_body = ""
    if st.button("Ejecutar"):
        try:
            request_body = json.loads(request_body)
            try:
                # timeout=10 porque puede demorar dado que es un servicio serverless
                response_body = request_mlservice(json=request_body, timeout=10)
            except json.JSONDecodeError:
                st.error("Invalid JSON in response body.")
            except httpx.RequestError as e:
                st.error(f"HTTP request failed: {e}")
        except json.JSONDecodeError:
            st.error("Invalid JSON in request body.")

    if response_body == "":
        return

    st.subheader("Respuesta JSON")
    st.json(response_body)
