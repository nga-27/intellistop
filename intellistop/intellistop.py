""" intellistop.py """
from typing import Union, Tuple, List

import numpy as np

from .libs import (
    download_data, ConfigProperties, VFStopsResultType, get_fourier_spectrum,
    calculate_time_series_variances, simple_moving_average_filter, smart_moving_average,
    SmartMovingAvgType, get_slope_of_data_set, generate_stop_loss_data_set, VFTimeSeriesType,
    CurrentStatusType
)

class IntelliStop:
    """ Intellistop class and functioning object """
    config: ConfigProperties = {}
    data = {}
    fund_name = ""
    benchmark = "^GSPC"
    latest_results = None
    stops = VFStopsResultType()
    smart_moving_avg = SmartMovingAvgType()
    has_errors = False

    def __init__(self, config: Union[dict, None] = None):
        if not config:
            config = {}
        self.config = ConfigProperties(config)


    def update_config(self, config: Union[dict, None] = None):
        """update_config

        Update the Intellistop config settings

        Args:
            config (Union[dict, None], optional): see available settings. Defaults to None.
        """
        if not config:
            config = {}
        self.config = ConfigProperties(config)


    def get_correct_pricing_key(self, data_set: dict) -> str:
        """get_correct_pricing_key

        Automatically determine if price key is 'Close' (most of them) or 'Adj Close' (for mutual
        funds, specifically)

        Args:
            data_set (dict): [modified] yfinance dictionary of stock data, with typical 'OCHLVD'
                            keys, where 'D' is date

        Returns:
            str: key that matches the type of fund
        """
        if self.has_errors:
            return 'Close'
        test_set = {
            data_set['Close'][3],
            data_set['Open'][3],
            data_set['High'][3],
            data_set['Low'][3]
        }
        if len(test_set) == 1:
            return 'Adj Close'
        return 'Close'


    def fetch_extended_time_series(self, fund: str) -> dict:
        """fetch_extended_time_series

        Pull data using yf api. For now, we'll default to a period of '5y' for analysis

        Args:
            fund (str): ticker symbol of the trade

        Returns:
            dict: data dict of 'OCHLVD' data, where 'D' is date. Format is nested:
                {
                    'SPY': {
                        'Open': [],
                        ...
                    }
                }
        """
        self.fund_name = fund
        self.config.yf_properties.period = '5y'
        self.config.yf_properties.start_date = None
        self.config.yf_properties.end_date = None
        self.data = download_data(fund, self.config)

        if len(self.data[self.fund_name]['Close']) == 0:
            self.has_errors = True

        self.config.vf_properties.pricing = self.get_correct_pricing_key(self.data[self.fund_name])
        return self.data


    def return_data(self, fund="", key: Union[str, None] = None) -> Union[dict, list]:
        """return_data

        Returns the full ticker data as a dict or a list, if supplied the ticker data object key

        Args:
            fund (str, optional): ticker string. Defaults to "".
            key (Union[str, None], optional): ticker dict object key, will return a list. Defaults
                to None.

        Returns:
            Union[dict, list]: ticker dict object or list
        """
        if key and key == '__full__' and fund != "":
            return self.data[fund]
        if not key:
            key = self.config.vf_properties.pricing
        if len(fund) > 0:
            return self.data[fund][key]
        return self.data


    def calculate_vf_stops_data(self) -> VFStopsResultType:
        """calculate_vf_stops_data

        Generate the stop loss / VF data

        Returns:
            VFStopsResultType
        """
        # pylint: disable=too-many-locals
        if self.has_errors:
            return self.stops

        data_key = self.config.vf_properties.pricing
        current_max = max(self.data[self.fund_name][data_key])
        self.stops.current_status.max_price = current_max
        self.stops.current_status.max_price_date = self.data[self.fund_name][data_key].index(current_max)
        self.stops.fund_name = self.fund_name

        sma = simple_moving_average_filter(self.data[self.fund_name][data_key], filter_size=200)
        lp_dataset = [datum - sma[i] for i, datum in enumerate(self.data[self.fund_name][data_key])]
        _, _, top_10 = get_fourier_spectrum({data_key: lp_dataset}, key=data_key)

        for is_derived in [False, True]:
            variances, _ = calculate_time_series_variances(
                lp_dataset,
                overrides={
                    'window': int(min(top_10)),
                    'mode': 'std',
                    'use_derived': is_derived
                }
            )

            truthy_vars = []
            falsy_vars = []
            for i, datum in enumerate(self.data[self.fund_name][data_key]):
                if datum > sma[i]:
                    truthy_vars.append(variances[i])
                if datum < sma[i]:
                    falsy_vars.append(variances[i])

            truthy_mean = np.mean(truthy_vars)
            falsy_mean = np.mean(falsy_vars)

            root_sq_mean = np.sqrt((truthy_mean ** 2) + (falsy_mean ** 2))
            root_sq_fraction = (3.0 * root_sq_mean) \
                / np.average(self.data[self.fund_name][data_key]) * 100.0
            root_sq_sl = max(self.data[self.fund_name][data_key]) \
                * (1.0 - (root_sq_fraction / 100.0))

            if is_derived:
                self.stops.derived.vf = root_sq_fraction
                self.stops.derived.stop_loss = root_sq_sl
            else:
                self.stops.alternate.vf = root_sq_fraction
                self.stops.alternate.stop_loss = root_sq_sl

        self.stops.stop_loss.aggressive = np.min(
            [self.stops.derived.stop_loss, self.stops.alternate.stop_loss]
        )
        self.stops.stop_loss.average = np.average(
            [self.stops.derived.stop_loss, self.stops.alternate.stop_loss]
        )
        self.stops.stop_loss.curated = self.stops.stop_loss.average
        self.stops.stop_loss.conservative = np.max(
            [self.stops.derived.stop_loss, self.stops.alternate.stop_loss]
        )

        self.stops.vf.conservative = np.min(
            [self.stops.derived.vf, self.stops.alternate.vf]
        )
        self.stops.vf.average = np.average([self.stops.derived.vf, self.stops.alternate.vf])
        self.stops.vf.curated = self.stops.vf.average
        self.stops.vf.aggressive = np.max([self.stops.derived.vf, self.stops.alternate.vf])

        if self.stops.vf.average > 50.0:
            self.stops.vf.curated = 50.0
            self.stops.stop_loss.curated = max(self.data[self.fund_name][data_key]) \
                * (1.0 - (self.stops.vf.curated / 100.0))

        return self.stops


    def generate_smart_moving_average(self) -> Tuple[list, list, list]:
        """generate_smart_moving_average

        Returns:
            Tuple[list, list, list]: SmartMovingAverage (SmMA), Short-term slope of SmMA,
                                    Long-term slope (SmMA)
        """
        if self.has_errors:
            return ([], [], [])

        data_key = self.config.vf_properties.pricing
        price_data = self.data[self.fund_name][data_key]
        window = 200 + int((self.stops.vf.curated - 25.0) / 4.0 * 3.0)

        self.smart_moving_avg.data_set = smart_moving_average(price_data, window)
        slope = get_slope_of_data_set(self.smart_moving_avg.data_set)

        short_window = 15
        long_window = 50
        self.smart_moving_avg.short_slope = simple_moving_average_filter(slope, short_window)
        self.smart_moving_avg.long_slope = simple_moving_average_filter(slope, long_window)

        # Because of how we generate the SMAs for x < filter_size, we want to just 0 them out to as
        # avoid any oddities with the "re-entry" algorithm
        self.smart_moving_avg.short_slope[0:window + short_window] = [0.0] * (window + short_window)
        self.smart_moving_avg.long_slope[0:window + long_window] = [0.0] * (window + long_window)

        return (
            self.smart_moving_avg.data_set,
            self.smart_moving_avg.short_slope,
            self.smart_moving_avg.long_slope
        )


    def analyze_data_set(self) -> List[VFTimeSeriesType]:
        """analyze_data_set

        Generate the actual analysis for the intellistop data set

        Returns:
            list: list of VFTimeSeriesType
        """
        if self.has_errors:
            return []

        # Because the market typically goes up over time, we'll assume we start each 5y series
        # with an "uptrend" and therefore stop-loss mode
        data = self.data[self.fund_name][self.config.vf_properties.pricing]
        volatility_factor = self.stops.vf.curated

        self.stops.data_sets, self.stops.event_log = generate_stop_loss_data_set(
            data,
            volatility_factor,
            self.smart_moving_avg.data_set,
            self.smart_moving_avg.short_slope,
            self.smart_moving_avg.long_slope
        )

        self.stops.current_status.max_price = np.round(self.stops.data_sets[-1].max_price, 2)
        self.stops.current_status.max_price_date = self.data[self.fund_name]['Date']\
            [self.stops.data_sets[-1].max_price_index]
        
        if self.stops.data_sets[-1].time_index_list[-1] != len(data) - 1:
            self.stops.current_status.status = CurrentStatusType.stopped_out
        else:
            if data[-1] > self.stops.data_sets[-1].caution_line[-1]:
                self.stops.current_status.status = CurrentStatusType.active_zone
            else:
                self.stops.current_status.status = CurrentStatusType.caution_zone

        print(self.stops.current_status.status)

        return self.stops.data_sets


    ##########################################################################################
    # ACTUAL FUNCTION
    ##########################################################################################

    def run_analysis_for_ticker(self, fund: str) -> VFStopsResultType:
        """run_analysis_for_ticker

        High-level function that runs all Intellistop functionality, a single function to run

        Args:
            fund (str): ticker symbol (e.g. "SPY")

        Returns:
            VFStopsResultType: The full results of the function:

                    derived: VFStopLossRawResultType
                    alternate: VFStopLossRawResultType
                    vf: VFStopLossResultType
                    stop_loss: VFStopLossResultType
                    current_max: float
                    fund_name: str
                    data_sets: List[VFTimeSeriesType]
                    event_log: list
        """
        print(f"Starting 'Intellistop' with fund ticker '{fund}'...")
        self.fetch_extended_time_series(fund)
        self.calculate_vf_stops_data()
        self.generate_smart_moving_average()
        self.analyze_data_set()

        return self.stops
