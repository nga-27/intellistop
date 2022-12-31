from enum import Enum
from typing import Union, List

from .constants import YF_DATA_CONFIG_DEFAULTS

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


class VFProperties:
    pricing: str = 'Close'


class VFStopLossResultType:
    aggressive: float
    average: float
    conservative: float
    curated: float

    def __init__(self):
        self.aggressive = 0.0
        self.average = 0.0
        self.conservative = 0.0
        self.curated = 0.0

class VFStopLossRawResultType:
    stop_loss: float
    vf: float

    def __init__(self):
        self.stop_loss = 0.0
        self.vf = 0.0

class VFTimeSeriesType:
    max_price: float
    caution_line: List[float]
    stop_loss_line: List[float]
    time_index_list: List[int]

    def __init__(self):
        self.max_price = 0.0
        self.caution_line = []
        self.stop_loss_line = []
        self.time_index_list = []

class StopLossEventType(Enum):
    stop = 'stop'
    minimum = 'minimum'
    activate = 'activate'

class StopLossEventLogType:
    index: int
    event: StopLossEventType
    price: float

    def __init__(self):
        self.index = 0
        self.event = StopLossEventType.stop
        self.price = 0.0


class VFStopsResultType:
    derived: VFStopLossRawResultType
    alternate: VFStopLossRawResultType
    vf: VFStopLossResultType
    stop_loss: VFStopLossResultType
    current_max: float
    fund_name: str
    data_sets: List[VFTimeSeriesType]
    event_log: List[StopLossEventLogType]

    def __init__(self):
        self.fund_name = ""
        self.current_max = 0.0
        self.alternate = VFStopLossRawResultType()
        self.derived = VFStopLossRawResultType()
        self.vf = VFStopLossResultType()
        self.stop_loss = VFStopLossResultType()
        self.data_sets = []
        self.event_log = []


class SmartMovingAvgType:
    data_set: list
    short_slope: list
    long_slope: list

    def __init__(self):
        self.data_set = []
        self.short_slope = []
        self.long_slope = []


################################################################

class ConfigProperties:
    yf_properties = YFProperties()
    vf_properties = VFProperties()

    def __init__(self, config: dict = {}):
        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)
        self.yf_properties.start_date = config.get("start_date")
        self.yf_properties.end_date = config.get("end_date")
        self.yf_properties.include_bench = config.get("include_bench", self.yf_properties.include_bench)

        self.vf_properties.pricing = config.get("vf_properties_pricing", self.vf_properties.pricing)
