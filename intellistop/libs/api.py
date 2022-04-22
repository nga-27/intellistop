import datetime

import yfinance as yf
import pandas as pd

CONFIG_DEFAULTS = {
    "period": "5y",
    "interval": "1d"
}

def download_data(fund: str, config: dict=CONFIG_DEFAULTS) -> dict:
    period = config.get('period', CONFIG_DEFAULTS["period"])
    interval = config.get('interval', CONFIG_DEFAULTS["interval"])
    fund += " ^GSPC"
    data = yf.download(tickers=fund, period=period, interval=interval, group_by='ticker')
    formatted_data = data_format(data)
    return formatted_data


def data_format(yf_data: pd.DataFrame) -> dict:
    corrected_data = {}
    for col in yf_data.columns:
        if col[0] not in corrected_data:
            corrected_data[col[0]] = {}
        corrected_data[col[0]][col[1]] = {}
    for fund_name in corrected_data:
        corrected_data[fund_name]["Date"] = [date.strftime("%Y-%m-%d") for date in yf_data[fund_name].index]
        for column in corrected_data[fund_name]:
            if column != "Date":
                corrected_data[fund_name][column] = [price for price in yf_data[fund_name][column].values]

    return corrected_data


