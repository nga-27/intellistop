import json

from .constants import YF_DATA_CONFIG_DEFAULTS

class YFProperties:
    period: str = ""
    interval: str = ""

    def __init__(self, property_dict: dict={}):
        self.period = property_dict.get("period", YF_DATA_CONFIG_DEFAULTS["period"])
        self.interval = property_dict.get("interval", YF_DATA_CONFIG_DEFAULTS["interval"])

    def serialize(self):
        return vars(self)


class ConfigProperties:
    yf_properties = YFProperties()

    def __init__(self, config: dict = {}):
        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)

