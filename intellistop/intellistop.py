from typing import List

from .libs import (
    download_data, calculate_momentum, get_beta, get_alpha, get_k_ratio,
    ConfigProperties, calculate_variances, run_vq_calculation, find_latest_max,
    VQStopsResultType, BetaPropertyEnum
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


    def calculate_stops(self) -> VQStopsResultType:
        results = VQStopsResultType()

        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark])
        fund_alpha = get_alpha(
            self.data[self.fund_name], self.data[self.benchmark], fund_beta[0], self.config
        )
        fund_k_ratio = get_k_ratio(self.data[self.fund_name], self.config)
        variances = calculate_variances(fund_momentum, self.config)
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


    def fetch_extended_time_series(self, fund: str):
        # For now, we'll just default to 5y of analysis
        self.fund_name = fund
        self.config.yf_properties.period = '5y'
        self.config.yf_properties.start_date = None
        self.config.yf_properties.end_date = None
        self.data = download_data(fund, self.config)
        return self.data


    def calculated_time_series_stops(self) -> List[VQStopsResultType]:
        results = list()

        ab_config = {
            "function": BetaPropertyEnum.BETA_ROLLING,
            "shift": 5
        }
        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark], properties=ab_config)
        return fund_beta