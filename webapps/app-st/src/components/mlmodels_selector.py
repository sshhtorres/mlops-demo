import streamlit as st

from config import get_app_config
from entities import MLServiceConfig
from utils.mlservices import get_mlservices_config_map
from utils.states import get_mlmodel_type_state_kv, get_mlmodel_service_url_state_kv


def on_selectbox():
    next_service_url = ""

    services = get_mlservices_config_map()
    (_, mtype) = get_mlmodel_type_state_kv()
    if mtype in services and services[mtype].service_url:
        next_service_url = services[mtype].service_url
    
    (skey, _) = get_mlmodel_service_url_state_kv()
    st.session_state[skey] = next_service_url


def render():
    services = get_mlservices_config_map()
    (skey, _) = get_mlmodel_type_state_kv()
    st.selectbox('Seleccione el tipo de modelo', services.keys(), key=skey, on_change=on_selectbox)

    (skey, url) = get_mlmodel_service_url_state_kv()
    st.text_input("Ingrese la URL del modelo",  key=skey)
