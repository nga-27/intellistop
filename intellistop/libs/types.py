from enum import Enum

from .constants import YF_DATA_CONFIG_DEFAULTS, MOMENTUM_CONFIG_DEFAULTS

class YFProperties:
    period: str = YF_DATA_CONFIG_DEFAULTS["period"]
    interval: str = YF_DATA_CONFIG_DEFAULTS["interval"]
    num_samples_per_calendar_year: int = 0

    def __init__(self):
        if "d" in self.interval:
            self.num_samples_per_calendar_year = 252
        if "w" in self.interval:
            self.num_samples_per_calendar_year = 52
        if "m" in self.interval:
            self.num_samples_per_calendar_year = 12


class MomentumCalculation(Enum):
    STANDARD = 0
    DIFFERENCE = 1

class MomentumProperties:
    period: int = MOMENTUM_CONFIG_DEFAULTS["period"]
    metric: str = MOMENTUM_CONFIG_DEFAULTS["metric"]
    calculator: MomentumCalculation = MomentumCalculation.STANDARD


class KRatioAlgorithms(Enum):
    YR_1996 = 1996,
    YR_2003 = 2003,
    YR_2013 = 2013

class KRatioProperties:
    is_log: bool = False
    algorithm: KRatioAlgorithms = KRatioAlgorithms.YR_2013


class VarianceComponents:
    total_var: float = 0.0
    total_std: float = 0.0
    negative_var: float = 0.0
    negative_std: float = 0.0


class VQProperties:
    std_level: int = 2

################################################################

class ConfigProperties:
    yf_properties = YFProperties()
    momentum_properties = MomentumProperties()
    k_ratio_properties = KRatioProperties()
    vq_properties = VQProperties()

    def __init__(self, config: dict = {}):
        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)
        self.momentum_properties.period = config.get("momentum_period", self.momentum_properties.period)
        self.momentum_properties.metric = config.get("momentum_metric", self.momentum_properties.metric)
        self.momentum_properties.calculator = config.get("momentum_calculator", self.momentum_properties.calculator)
        self.k_ratio_properties.is_log = config.get("k_ratio_is_log", self.k_ratio_properties.is_log)
        self.k_ratio_properties.algorithm = config.get("k_ratio_algorithm", self.k_ratio_properties.algorithm)
        self.vq_properties.std_level = config.get("vq_properties_level", self.vq_properties.std_level)
