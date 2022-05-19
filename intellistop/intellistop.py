from .libs import (
    download_data, calculate_momentum, get_beta, get_alpha, get_k_ratio,
    ConfigProperties, calculate_variances, run_vq_calculation, find_latest_max
)

class IntelliStop:
    config: ConfigProperties = {}
    data = {}
    fund_name = ""
    benchmark = "^GSPC"

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


    def calculate_stops(self):
        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark])
        fund_alpha = get_alpha(
            self.data[self.fund_name], self.data[self.benchmark], fund_beta, self.config
        )
        fund_k_ratio = get_k_ratio(self.data[self.fund_name], self.config)
        variances = calculate_variances(fund_momentum, self.config)
        _vq = run_vq_calculation(fund_beta, fund_alpha, variances, fund_k_ratio, self.config)
        _max = find_latest_max(self.data[self.fund_name]['Close'])
        stop_loss = _max * (100.0 - _vq) / 100.0
        print(f"current: {self.data[self.fund_name]['Close'][-1]}, stop: {_vq} --> ${stop_loss}")
        return stop_loss
