from copy import deepcopy

from .libs import download_data, calculate_momentum, ConfigProperties

class IntelliStop:
    config: ConfigProperties = {}
    data = {}
    fund_name = ""

    def __init__(self, config: dict = {}):
        self.config = ConfigProperties(config)


    def fetch_data(self, fund: str):
        self.fund_name = fund
        self.data = download_data(fund, self.config)
        return self.data


    def calculate_stops(self):
        fund_momentum = calculate_momentum(self.data[self.fund_name], self.config)
        print("stops")
