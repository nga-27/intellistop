import yfinance as yf
import pandas as pd

from .lib_types import ConfigProperties


def download_data(fund: str, config: ConfigProperties) -> dict:
    period = config.yf_properties.period
    interval = config.yf_properties.interval
    start_date = config.yf_properties.start_date
    end_date = config.yf_properties.end_date

    if config.yf_properties.include_bench:
        fund += " ^GSPC"

    if start_date and end_date:
        data = yf.download(
            tickers=fund,
            start=start_date,
            end=end_date,
            interval=interval,
            group_by='ticker'
        )
    elif start_date:
        data = yf.download(tickers=fund, start=start_date, interval=interval, group_by='ticker')
    else:
        data = yf.download(tickers=fund, period=period, interval=interval, group_by='ticker')
    formatted_data = data_format(data, fund)
    return formatted_data


def data_format(yf_data: pd.DataFrame, fund_name: str) -> dict:
    corrected_data = {}

    if 'Close' in yf_data.columns:
        # Single fund that's not in the "multiIndex" format
        corrected_data[fund_name] = {}
        for col in yf_data.columns:
            corrected_data[fund_name][col] = {}
        corrected_data[fund_name]["Date"] = [date.strftime("%Y-%m-%d") for date in yf_data.index]
        for column in corrected_data[fund_name]:
            if column != "Date":
                # pylint: disable=unnecessary-comprehension
                corrected_data[fund_name][column] = [price for price in yf_data[column].values]

    else:
        for col in yf_data.columns:
            if col[0] not in corrected_data:
                corrected_data[col[0]] = {}
            corrected_data[col[0]][col[1]] = {}

        for fund_ticker in corrected_data:
            corrected_data[fund_ticker]["Date"] = [
                date.strftime("%Y-%m-%d") for date in yf_data[fund_ticker].index]
            for column in corrected_data[fund_ticker]:
                if column != "Date":
                    corrected_data[fund_ticker][column] = [
                        price for price in yf_data[fund_ticker][column].values]

    return corrected_data
