from requests import get
from .libs import (
    download_data, calculate_momentum, get_beta, get_alpha, get_k_ratio,
    ConfigProperties, calculate_variances, VarianceComponents
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


    def calculate_stops(self):
        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        fund_beta = get_beta(self.data[self.fund_name], self.data[self.benchmark])
        fund_alpha = get_alpha(
            self.data[self.fund_name], self.data[self.benchmark], fund_beta, self.config
        )
        fund_k_ratio = get_k_ratio(self.data[self.fund_name], self.config)
        variances = calculate_variances(fund_momentum, self.config)
        print(f"stops {fund_momentum[14]}")
