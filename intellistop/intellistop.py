from typing import List

from .libs import (
    download_data, calculate_momentum, get_beta, get_alpha, get_k_ratio,
    ConfigProperties, calculate_variances, run_vq_calculation, find_latest_max,
    VQStopsResultType, BetaPropertyEnum, get_daily_gains, VarianceProperties,
    windowed_filter, subtraction_filter, fourier_spectrum, calculate_time_series_variances,
    simple_moving_average_filter
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

    def get_variances(self, data, config: ConfigProperties) -> list:
        if config.variance_components.variance_type == VarianceProperties.VARIANCE_PRICE:
            fund_performance = get_daily_gains(data)
            print(f"***RANGES: {min(fund_performance)} -> {max(fund_performance)}")
            variances = calculate_variances(fund_performance, config)

        elif config.variance_components.variance_type == VarianceProperties.VARIANCE_WINDOWED:
            windowed_data = windowed_filter(data['Close'], props=self.config.filter_properties)
            normalized_data = subtraction_filter(data['Close'], windowed_data)
            print(f"***RANGES: {min(normalized_data)} -> {max(normalized_data)}")
            variances = calculate_variances(normalized_data, config)

        else:
            fund_momentum = calculate_momentum(data, config)
            print(f"***RANGES: {min(fund_momentum)} -> {max(fund_momentum)}")
            variances = calculate_variances(fund_momentum, config)
        return variances


    def calculate_stops(self) -> VQStopsResultType:
        results = VQStopsResultType()

        variances = self.get_variances(self.data[self.fund_name], self.config)

        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark])
        fund_alpha = get_alpha(
            self.data[self.fund_name], self.data[self.benchmark], fund_beta[0], self.config
        )
        fund_k_ratio = get_k_ratio(self.data[self.fund_name], self.config)            

        _vq = run_vq_calculation(fund_beta[0], fund_alpha, variances, fund_k_ratio, self.config)
        _max = find_latest_max(self.data[self.fund_name]['Close'])
        stop_loss = _max * (100.0 - _vq) / 100.0
        print(f"current: {self.data[self.fund_name]['Close'][-1]}, stop: {_vq} --> ${stop_loss}")

        results.stop_loss = stop_loss
        results.vq = _vq
        self.latest_results = results
        return results

    
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


    def calculated_time_series_stops(self, use_derived = False) -> List[VQStopsResultType]:
        results = list()

        ab_config = {
            "function": BetaPropertyEnum.BETA_ROLLING,
            "shift": 5
        }
        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark], properties=ab_config)
        variances = calculate_variances(fund_momentum, self.config, overrides={"variance_type": VarianceProperties.VARIANCE_ROLLING, "shift": 5})

        sma = simple_moving_average_filter(self.data[self.fund_name]['Close'], filter_size=200)
        lp_dataset = [datum - sma[i] for i, datum in enumerate(self.data[self.fund_name]['Close'])]
        # x_fft, y_fft, top_5 = fourier_spectrum(self.data[self.fund_name])
        x_fft, y_fft, top_5 = fourier_spectrum({'Close': lp_dataset})
        # variances, window = calculate_time_series_variances(self.data[self.fund_name], overrides={'window': int(min(top_5)), 'mode': 'std'})
        variances, window = calculate_time_series_variances({'Close': lp_dataset}, overrides={'window': int(min(top_5)), 'mode': 'std', 'use_derived': use_derived})
        return x_fft, y_fft, top_5, variances, window, sma, lp_dataset