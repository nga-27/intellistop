from typing import Union

import numpy as np

from .libs import (
    download_data, ConfigProperties, VQStopsResultType, get_fourier_spectrum,
    calculate_time_series_variances, simple_moving_average_filter, get_extrema,
    exponential_moving_average_filter, weighted_moving_average_filter,
    smart_moving_average
)

class IntelliStop:
    config: ConfigProperties = {}
    data = {}
    fund_name = ""
    benchmark = "^GSPC"
    latest_results = None
    stops = VQStopsResultType()

    def __init__(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def update_config(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def fetch_data(self, fund: str):
        self.fund_name = fund
        self.data = download_data(fund, self.config)
        return self.data


    def return_data(self, fund="", key: Union[str, None] = None):
        if len(fund) > 0:
            if key:
                return self.data[fund][key]
            return self.data[fund]
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
        self.stops.stop_loss.conservative = np.max([self.stops.derived.stop_loss, self.stops.alternate.stop_loss])

        self.stops.vq.conservative = np.min([self.stops.derived.vq, self.stops.alternate.vq])
        self.stops.vq.average = np.average([self.stops.derived.vq, self.stops.alternate.vq])
        self.stops.vq.aggressive = np.max([self.stops.derived.vq, self.stops.alternate.vq])

        return self.stops


    def generate_smart_moving_average(self):
        data_key = self.config.vq_properties.pricing
        price_data = self.data[self.fund_name][data_key]
        window = 200 + int((self.stops.vq.average - 25.0) / 4.0 * 3.0)

        simple_ma = simple_moving_average_filter(price_data, window)
        smart_ma = smart_moving_average(price_data, window)

        lp_data = [price - simple_ma[i] for i, price in enumerate(price_data)]
        overcome = (self.stops.vq.average / 100.0) / 3.0 * 2.0
        extrema_list = get_extrema({data_key: lp_data}, overcome_pct=overcome, key=data_key)
        return extrema_list, lp_data, simple_ma, smart_ma


    # def get_variances(self, data, config: ConfigProperties) -> list:
    #     if config.variance_components.variance_type == VarianceProperties.VARIANCE_PRICE:
    #         fund_performance = get_daily_gains(data)
    #         variances = calculate_variances(fund_performance, config)

    #     elif config.variance_components.variance_type == VarianceProperties.VARIANCE_WINDOWED:
    #         windowed_data = windowed_filter(data['Close'], props=self.config.filter_properties)
    #         normalized_data = subtraction_filter(data['Close'], windowed_data)
    #         variances = calculate_variances(normalized_data, config)

    #     else:
    #         fund_momentum = calculate_momentum(data, config)
    #         variances = calculate_variances(fund_momentum, config)
    #     return variances


    # def calculate_stops_deprecated(self) -> VQStopsResultType:
    #     results = VQStopsResultType()

    #     variances = self.get_variances(self.data[self.fund_name], self.config)

    #     fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark])
    #     fund_alpha = get_alpha(
    #         self.data[self.fund_name], self.data[self.benchmark], fund_beta[0], self.config
    #     )
    #     fund_k_ratio = get_k_ratio(self.data[self.fund_name], self.config)            

    #     _vq = run_vq_calculation(fund_beta[0], fund_alpha, variances, fund_k_ratio, self.config)
    #     _max = find_latest_max(self.data[self.fund_name]['Close'])
    #     stop_loss = _max * (100.0 - _vq) / 100.0

    #     results.stop_loss = stop_loss
    #     results.vq = _vq
    #     self.latest_results = results
    #     return results

    
    def get_latest_results(self):
        return self.latest_results


    def fetch_extended_time_series(self, fund: str) -> dict:
        # For now, we'll just default to 5y of analysis
        self.fund_name = fund
        self.config.yf_properties.period = '5y'
        self.config.yf_properties.start_date = None
        self.config.yf_properties.end_date = None
        self.data = download_data(fund, self.config)
        return self.data
