from enum import Enum
from typing import Union

from .constants import YF_DATA_CONFIG_DEFAULTS, MOMENTUM_CONFIG_DEFAULTS

class YFProperties:
    period: str = YF_DATA_CONFIG_DEFAULTS["period"]
    interval: str = YF_DATA_CONFIG_DEFAULTS["interval"]
    start_date: Union[str,None] = None
    end_date: Union[str,None] = None
    num_samples_per_calendar_year: int = 0
    include_bench: bool = False

    def __init__(self):
        # We're assuming 1 of everything. Note "m" is minute
        if "d" in self.interval:
            self.num_samples_per_calendar_year = 252
        if "wk" in self.interval:
            self.num_samples_per_calendar_year = 52
        if "mo" in self.interval:
            self.num_samples_per_calendar_year = 12


class MomentumCalculation(Enum):
    STANDARD = 0,
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


class VarianceProperties(Enum):
    VARIANCE_MOMENTUM = 0,
    VARIANCE_PRICE = 1,
    VARIANCE_WINDOWED = 2,
    VARIANCE_ROLLING = 3

class VarianceComponents:
    total_var: Union[float, list] = 0.0
    total_std: Union[float, list]
    negative_var: Union[float, list] = 0.0
    negative_std: Union[float, list] = 0.0
    variance_type: VarianceProperties
    shift: int
    window: int
    match_length: bool

    def __init__(self, config: dict = {}):
        self.variance_type = config.get("variance_type", VarianceProperties.VARIANCE_MOMENTUM)
        self.shift = config.get('shift', 0)
        self.window = config.get('window', 252)
        self.match_length = config.get('match_length', True)


class VQProperties:
    std_level: int = 2
    pricing: str = 'Close'


class VQStopLossResultType:
    aggressive: float
    average: float
    conservative: float

    def __init__(self):
        self.aggressive = 0.0
        self.average = 0.0
        self.conservative = 0.0

class VQStopLossRawResultType:
    stop_loss: float
    vq: float

    def __init__(self):
        self.stop_loss = 0.0
        self.vq = 0.0

class VQStopsResultType:
    derived: VQStopLossRawResultType
    alternate: VQStopLossRawResultType
    vq: VQStopLossResultType
    stop_loss: VQStopLossResultType
    current_max: float
    fund_name: str

    def __init__(self):
        self.fund_name = ""
        self.current_max = 0.0
        self.alternate = VQStopLossRawResultType()
        self.derived = VQStopLossRawResultType()
        self.vq = VQStopLossResultType()
        self.stop_loss = VQStopLossResultType()


class BetaPropertyEnum(Enum):
    BETA_STANDARD = 0,
    BETA_ROLLING = 1

class BetaProperties:
    function: BetaPropertyEnum
    shift: int
    window: int
    match_length: bool

    def __init__(self, config: dict = {}):
        self.function = config.get('function', BetaPropertyEnum.BETA_STANDARD)
        self.shift = config.get('shift', 0)
        self.window = config.get('window', 252)
        self.match_length = config.get('match_length', True)


class FilterProperties:
    filter_half_width: int = 5

################################################################

class ConfigProperties:
    yf_properties = YFProperties()
    momentum_properties = MomentumProperties()
    k_ratio_properties = KRatioProperties()
    vq_properties = VQProperties()
    variance_components = VarianceComponents()
    filter_properties = FilterProperties()

    def __init__(self, config: dict = {}):
        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)
        self.yf_properties.start_date = config.get("start_date")
        self.yf_properties.end_date = config.get("end_date")
        self.yf_properties.include_bench = config.get("include_bench", self.yf_properties.include_bench)

        self.momentum_properties.period = config.get("momentum_period", self.momentum_properties.period)
        self.momentum_properties.metric = config.get("momentum_metric", self.momentum_properties.metric)
        self.momentum_properties.calculator = config.get("momentum_calculator", self.momentum_properties.calculator)

        self.k_ratio_properties.is_log = config.get("k_ratio_is_log", self.k_ratio_properties.is_log)
        self.k_ratio_properties.algorithm = config.get("k_ratio_algorithm", self.k_ratio_properties.algorithm)

        self.vq_properties.std_level = config.get("vq_properties_level", self.vq_properties.std_level)
        self.vq_properties.pricing = config.get("vq_properties_pricing", self.vq_properties.pricing)
        self.variance_components.variance_type = config.get("variance_type", self.variance_components.variance_type)

        self.filter_properties.filter_half_width = config.get("filter_half_width", self.filter_properties.filter_half_width)
