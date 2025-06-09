from typing import Any

from pydantic import BaseModel


class StateMap(BaseModel):
    def get_default_state_values(self)-> dict[str, Any]:
        raise NotImplementedError()


class MLModelSelectionMap(StateMap):
    mlmodel_type: str = "components.mlmodel_selection.mlmodel_type"
    mlservice_url: str = "components.mlmodel_selection.mlservice_url"

    def get_default_state_values(self):
        return {
            "mlmodel_type": "",
            "mlservice_url": ""
        }


class AppMap(StateMap):
    mlmodel_selection: MLModelSelectionMap = MLModelSelectionMap()

    def get_default_state_values(self):
        return {}
