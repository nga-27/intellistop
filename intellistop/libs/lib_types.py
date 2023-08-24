""" library types """
from enum import Enum
from typing import Union, List

from .constants import YF_DATA_CONFIG_DEFAULTS

class YFProperties:
    """ Yahoo Finance Properties """
    # pylint: disable=too-few-public-methods
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
    """ Volatility Factor Properties """
    # pylint: disable=too-few-public-methods
    pricing: str = 'Close'


class VFStopLossResultType:
    """ Volatility Factor / Stop Loss Result Type """
    # pylint: disable=too-few-public-methods
    aggressive: float
    average: float
    conservative: float
    curated: float
    historical_cons: float

    def __init__(self):
        self.aggressive = 0.0
        self.average = 0.0
        self.conservative = 0.0
        self.curated = 0.0
        self.historical_cons = 0.0

class VFStopLossRawResultType:
    """ Volatility Factor / Stop Loss Raw Result Type"""
    # pylint: disable=too-few-public-methods,invalid-name
    stop_loss: float
    vf: float

    def __init__(self):
        self.stop_loss = 0.0
        self.vf = 0.0

class VFTimeSeriesType:
    """ Volatility Factor Time Series Type """
    # pylint: disable=too-few-public-methods
    max_price: float
    max_price_index: int
    caution_line: List[float]
    stop_loss_line: List[float]
    conservative_line: List[float]
    time_index_list: List[int]

    def __init__(self):
        self.max_price = 0.0
        self.max_price_index = 0
        self.caution_line = []
        self.stop_loss_line = []
        self.conservative_line = []
        self.time_index_list = []

class StopLossEventType(Enum):
    """ Stop Loss Event Type Enumeration """
    STOP = 'stop'
    MINIMUM = 'minimum'
    ACTIVATE = 'activate'

class StopLossEventLogType:
    """ Stop Loss Event Log Type """
    # pylint: disable=too-few-public-methods
    index: int
    event: StopLossEventType
    price: float

    def __init__(self):
        self.index = 0
        self.event = StopLossEventType.STOP
        self.price = 0.0


class CurrentStatusType(Enum):
    """ Current Status Type Enumeration """
    ACTIVE_ZONE = "active_zone"
    CAUTION_ZONE = "caution_zone"
    CONSERVATIVE_OUT = "conservative_out"
    STOPPED_OUT = "stopped_out"


class CurrentInfoType:
    """ Current Info Type """
    # pylint: disable=too-few-public-methods
    max_price: float
    max_price_date: str
    status: CurrentStatusType

    def __init__(self, price = 0.0, date = ""):
        self.max_price = price
        self.max_price_date = date
        self.status = CurrentStatusType.ACTIVE_ZONE


class VFStopsResultType:
    """ Volatility Factor / Stops Result Type (the main object returned) """
    # pylint: disable=too-few-public-methods,invalid-name,too-many-instance-attributes
    derived: VFStopLossRawResultType
    alternate: VFStopLossRawResultType
    vf: VFStopLossResultType
    stop_loss: VFStopLossResultType
    current_status: CurrentInfoType
    fund_name: str
    data_sets: List[VFTimeSeriesType]
    event_log: List[StopLossEventLogType]

    def __init__(self):
        self.fund_name = ""
        self.current_status = CurrentInfoType()
        self.alternate = VFStopLossRawResultType()
        self.derived = VFStopLossRawResultType()
        self.vf = VFStopLossResultType()
        self.stop_loss = VFStopLossResultType()
        self.data_sets = []
        self.event_log = []


class IntelligentMovingAvgType:
    """ Intelligent Moving Average Type """
    # pylint: disable=too-few-public-methods
    data_set: list
    short_slope: list
    long_slope: list

    def __init__(self):
        self.data_set = []
        self.short_slope = []
        self.long_slope = []


class NewTickerDataStorageType:
    """ New Ticker Data Storage for Storage Class """
    # pylint: disable=too-few-public-methods
    current_stop: float
    current_vf: float
    current_max_price: float

    def __init__(self, current_vf: float, stop: float, max_close: float):
        self.current_stop = stop
        self.current_vf = current_vf
        self.current_max_price = max_close


################################################################

class ConfigProperties:
    """ Configuration Properties (high-level configuration settings) """
    # pylint: disable=too-few-public-methods
    yf_properties = YFProperties()
    vf_properties = VFProperties()

    def __init__(self, config: Union[dict, None] = None):
        if not config:
            config = {}

        self.yf_properties.interval = config.get("interval", self.yf_properties.interval)
        self.yf_properties.period = config.get("period", self.yf_properties.period)
        self.yf_properties.start_date = config.get("start_date")
        self.yf_properties.end_date = config.get("end_date")
        self.yf_properties.include_bench = config.get(
            "include_bench",
            self.yf_properties.include_bench
        )

        self.vf_properties.pricing = config.get("vf_properties_pricing", self.vf_properties.pricing)
