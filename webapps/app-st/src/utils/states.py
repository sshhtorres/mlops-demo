from typing import Any

import streamlit as st

from states import AppMap, StateMap


@st.cache_data
def get_app_state_mapping() -> AppMap:
    return AppMap()


def get_mlmodel_service_url_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.mlmodel_selection.mlservice_url
    value = st.session_state[key]
    return (key, value)


def get_mlmodel_type_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.mlmodel_selection.mlmodel_type
    value = st.session_state[key]
    return (key, value)


def map_session_state(sm: StateMap):
    defaults: dict[str, Any] = sm.get_default_state_values()
    for field, mapping in sm:
        if isinstance(mapping, StateMap):
            map_session_state(mapping)
        elif field in defaults:
            st.session_state[mapping] = defaults[field]
