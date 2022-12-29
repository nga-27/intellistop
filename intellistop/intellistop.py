from typing import Union

import numpy as np

from .libs import (
    download_data, ConfigProperties, VQStopsResultType, get_fourier_spectrum,
    calculate_time_series_variances, simple_moving_average_filter, smart_moving_average,
    SmartMovingAvgType, get_slope_of_data_set, get_stop_loss_from_value
)

class IntelliStop:
    config: ConfigProperties = {}
    data = {}
    fund_name = ""
    benchmark = "^GSPC"
    latest_results = None
    stops = VQStopsResultType()
    smart_moving_avg = SmartMovingAvgType()

    def __init__(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def update_config(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def get_correct_pricing_key(self, data_set: dict) -> str:
        test_set = {data_set['Close'][3], data_set['Open'][3], data_set['High'][3], data_set['Low'][3]}
        if len(test_set) == 1:
            return 'Adj Close'
        return 'Close'


    def fetch_data(self, fund: str):
        self.fund_name = fund
        self.data = download_data(fund, self.config)
        return self.data


    def fetch_extended_time_series(self, fund: str) -> dict:
        # For now, we'll just default to 5y of analysis
        self.fund_name = fund
        self.config.yf_properties.period = '5y'
        self.config.yf_properties.start_date = None
        self.config.yf_properties.end_date = None
        self.data = download_data(fund, self.config)
        self.config.vq_properties.pricing = self.get_correct_pricing_key(self.data[self.fund_name])
        return self.data


    def return_data(self, fund="", key: Union[str, None] = None):
        if not key:
            key = self.config.vq_properties.pricing
        if len(fund) > 0:
            return self.data[fund][key]
        return self.data


    def calculate_vq_stops_data(self) -> VQStopsResultType:
        data_key = self.config.vq_properties.pricing
        self.stops.current_max = max(self.data[self.fund_name][data_key])
        self.stops.fund_name = self.fund_name

        sma = simple_moving_average_filter(self.data[self.fund_name][data_key], filter_size=200)
        lp_dataset = [datum - sma[i] for i, datum in enumerate(self.data[self.fund_name][data_key])]
        _, _, top_10 = get_fourier_spectrum({data_key: lp_dataset}, key=data_key)

        for is_derived in [False, True]:
            variances, _ = calculate_time_series_variances(
                {data_key: lp_dataset},
                overrides={
                    'window': int(min(top_10)),
                    'mode': 'std',
                    'use_derived': is_derived
                },
                key=data_key
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
            root_sq_fraction = (3.0 * root_sq_mean) / np.average(self.data[self.fund_name][data_key]) * 100.0
            root_sq_sl = max(self.data[self.fund_name][data_key]) * (1.0 - (root_sq_fraction / 100.0))

            if is_derived:
                self.stops.derived.vq = root_sq_fraction
                self.stops.derived.stop_loss = root_sq_sl
            else:
                self.stops.alternate.vq = root_sq_fraction
                self.stops.alternate.stop_loss = root_sq_sl

        self.stops.stop_loss.aggressive = np.min([self.stops.derived.stop_loss, self.stops.alternate.stop_loss])
        self.stops.stop_loss.average = np.average([self.stops.derived.stop_loss, self.stops.alternate.stop_loss])
        self.stops.stop_loss.curated = self.stops.stop_loss.average
        self.stops.stop_loss.conservative = np.max([self.stops.derived.stop_loss, self.stops.alternate.stop_loss])

        self.stops.vq.conservative = np.min([self.stops.derived.vq, self.stops.alternate.vq])
        self.stops.vq.average = np.average([self.stops.derived.vq, self.stops.alternate.vq])
        self.stops.vq.curated = self.stops.vq.average
        self.stops.vq.aggressive = np.max([self.stops.derived.vq, self.stops.alternate.vq])

        if self.stops.vq.average > 50.0:
            self.stops.vq.curated = 50.0
            self.stops.stop_loss.curated = max(self.data[self.fund_name][data_key]) * (1.0 - (self.stops.vq.curated / 100.0))

        return self.stops


    def generate_smart_moving_average(self):
        data_key = self.config.vq_properties.pricing
        price_data = self.data[self.fund_name][data_key]
        window = 200 + int((self.stops.vq.curated - 25.0) / 4.0 * 3.0)

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

        return self.smart_moving_avg.data_set, self.smart_moving_avg.short_slope, self.smart_moving_avg.long_slope


    def analyze_data_set(self):
        # Because the market typically goes up over time, we'll assume we start each 5y series
        # with an "uptrend" and therefore stop-loss mode
        data = self.data[self.fund_name][self.config.vq_properties.pricing]
        vq = self.stops.vq.curated

        current_max = [0, data[0]]
        current_min = [0, 100.0 * data[0]]
        current_stop_losses = [0.0] * len(data)
        current_stop_losses[0] = get_stop_loss_from_value(data[0], vq)
        mode = 'active'
        reset_stop = [False, False, False, False, False]

        for i, price in enumerate(data):
            if mode == 'active':
                if price > current_max[1]:
                    current_max[1] = price
                    current_max[0] = i
                    current_stop_losses[i] = get_stop_loss_from_value(price, vq)
                else:
                    # We need to set anyway
                    current_stop_losses[i] = current_stop_losses[i-1]

            if price < current_stop_losses[i] and mode == 'active':
                # Officially a STOPPED OUT condition
                mode = 'stopped'
                current_max[1] = 0.0
                print(f"stopped: ${price}, index: {i}")

            if mode == 'stopped':
                # First, track minimum...
                if price < current_min[1]:
                    current_min[1] = price
                    current_min[0] = i
                    print(f"new min: ${price}, index: {i}")

                # Next, price has to rebound 1 VQ % (once)
                if price >= get_stop_loss_from_value(current_min[1], vq, isUpFrom=True) and not reset_stop[0]:
                    reset_stop[0] = True

                # Next, price has to be above the SmMA (on-going condition, thus the reset)
                if reset_stop[0] and price > self.smart_moving_avg.data_set[i]:
                    reset_stop[1] = True
                else:
                    reset_stop[1] = False

                # Next, short-time slope of SmMA must be > 0 (on-going)
                if reset_stop[1] and self.smart_moving_avg.short_slope[i] > 0.0:
                    reset_stop[2] = True
                else:
                    reset_stop[2] = False

                # Next, long-time slope of SmMA must be > 0 (on-going)
                if reset_stop[2] and self.smart_moving_avg.long_slope[i] > 0.0:
                    reset_stop[3] = True
                else:
                    reset_stop[3] = True

                # Finally, short_slope > long_slope (on-going)
                if reset_stop[3] and self.smart_moving_avg.short_slope[i] > self.smart_moving_avg.long_slope[i]:
                    reset_stop[4] = True

                if all(reset_stop):
                    # WE DID IT! We're back in!
                    mode = 'active'
                    reset_stop = [False for _ in reset_stop]
                    current_max[1] = price
                    current_max[0] = i
                    current_stop_losses[i] = get_stop_loss_from_value(price, vq)
                    print(f"back in: ${price}, index: {i}")

        return current_stop_losses
                
