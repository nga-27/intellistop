import numpy as np

from .libs import (
    download_data, ConfigProperties, VQStopsResultType, fourier_spectrum,
    calculate_time_series_variances, simple_moving_average_filter
)

class IntelliStop:
    config: ConfigProperties = {}
    data = {}
    fund_name = ""
    benchmark = "^GSPC"
    latest_results = None

    def __init__(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def update_config(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def fetch_data(self, fund: str):
        self.fund_name = fund
        self.data = download_data(fund, self.config)
        return self.data


    def return_data(self, fund=""):
        if len(fund) > 0:
            return self.data[fund]
        return self.data


    def calculate_vq_stops_data(self) -> VQStopsResultType:
        stops = VQStopsResultType()
        stops.current_max = max(self.data[self.fund_name]['Close'])
        stops.fund_name = self.fund_name

        sma = simple_moving_average_filter(self.data[self.fund_name]['Close'], filter_size=200)
        lp_dataset = [datum - sma[i] for i, datum in enumerate(self.data[self.fund_name]['Close'])]
        _, _, top_5 = fourier_spectrum({'Close': lp_dataset})

        for is_derived in [False, True]:
            variances, _ = calculate_time_series_variances(
                {'Close': lp_dataset},
                overrides={
                    'window': int(min(top_5)),
                    'mode': 'std',
                    'use_derived': is_derived
                }
            )

            truthy_vars = []
            falsy_vars = []
            for i, datum in enumerate(self.data[self.fund_name]['Close']):
                if datum > sma[i]:
                    truthy_vars.append(variances[i])
                if datum < sma[i]:
                    falsy_vars.append(variances[i])

            truthy_mean = np.mean(truthy_vars)
            falsy_mean = np.mean(falsy_vars)

            root_sq_mean = np.sqrt((truthy_mean ** 2) + (falsy_mean ** 2))
            root_sq_fraction = (3.0 * root_sq_mean) / np.average(self.data[self.fund_name]['Close']) * 100.0
            root_sq_sl = max(self.data[self.fund_name]['Close']) * (1.0 - (root_sq_fraction / 100.0))

            if is_derived:
                stops.derived.vq = root_sq_fraction
                stops.derived.stop_loss = root_sq_sl
            else:
                stops.alternate.vq = root_sq_fraction
                stops.alternate.stop_loss = root_sq_sl

        stops.stop_loss.aggressive = np.min([stops.derived.stop_loss, stops.alternate.stop_loss])
        stops.stop_loss.average = np.average([stops.derived.stop_loss, stops.alternate.stop_loss])
        stops.stop_loss.conservative = np.max([stops.derived.stop_loss, stops.alternate.stop_loss])

        stops.vq.conservative = np.min([stops.derived.vq, stops.alternate.vq])
        stops.vq.average = np.average([stops.derived.vq, stops.alternate.vq])
        stops.vq.aggressive = np.max([stops.derived.vq, stops.alternate.vq])

        return stops

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
