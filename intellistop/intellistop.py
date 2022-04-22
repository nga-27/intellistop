from copy import deepcopy
from .data import download_data, CONFIG_DEFAULTS

class IntelliStop:
    config = deepcopy(CONFIG_DEFAULTS)

    def __init__(self, config: dict = {}):
        if "period" in config:
            self.config["period"] = config["period"]
        if "interval" in config:
            self.config["interval"] = config["interval"]


    def fetch_data(self, fund: str):
        return download_data(fund, self.config)
