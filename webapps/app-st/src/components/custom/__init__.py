import os
from pathlib import Path

import streamlit.components.v1 as components


BASE_PATH = Path(os.path.dirname(__file__))
COMPONENTS_MAP = {}


def _declare_custom_component(id: str):
    component_path = BASE_PATH / id
    if not os.path.exists(component_path):
        raise RuntimeError(f'icesi: component path does not exist for id="{id}"')

    return components.declare_component(id, path=component_path)


def render_custom_component(id: str, **kwargs):
    if id in COMPONENTS_MAP:
        st_component = COMPONENTS_MAP[id]
    else:
        st_component = _declare_custom_component(id)
        COMPONENTS_MAP[id] = st_component

    return st_component(**kwargs)
