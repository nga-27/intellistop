import json

from .constants import YF_DATA_CONFIG_DEFAULTS, MOMENTUM_CONFIG_DEFAULTS

class YFProperties:
    period: str = ""
    interval: str = ""

    def __init__(self, property_dict: dict={}):
        self.period = property_dict.get("period", YF_DATA_CONFIG_DEFAULTS["period"])
        self.interval = property_dict.get("interval", YF_DATA_CONFIG_DEFAULTS["interval"])

    def serialize(self):
        return vars(self)

class MomentumProperties:
    period: int = 10
    metric: str = ""

    def __init__(self, property_dict: dict={}):
        self.period = property_dict.get("period", MOMENTUM_CONFIG_DEFAULTS["period"])
        self.metric = property_dict.get("metric", MOMENTUM_CONFIG_DEFAULTS["metric"])


class ConfigProperties:
    yf_properties = YFProperties()
    momentum_properties = MomentumProperties()

    def __init__(self, config: dict = {}):
        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)
        self.momentum_properties.period = config.get("momentum_period", self.momentum_properties.period)
        self.momentum_properties.metric = config.get("momentum_metric", self.momentum_properties.metric)
