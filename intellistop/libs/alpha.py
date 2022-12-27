# Essentially, it's: alpha = fund_perf - risk_free - beta * (bench_perf - risk_free)
# from matplotlib import pyplot as plt
from intellistop.libs.lib_types import ConfigProperties
from .api import download_data

ONE_YEAR_TRADE_DAYS = 252
RISK_FREE_FUND = "^TNX" # 10 year treasury
# RISK_FREE_FUND = "^IRX"

def get_alpha(fund: dict, benchmark: dict, beta: float, config: ConfigProperties) -> float:
    risk_free = download_data(RISK_FREE_FUND, config)[RISK_FREE_FUND]['Close']
    one_yr_fund = (fund['Adj Close'][-1] - fund["Adj Close"][-ONE_YEAR_TRADE_DAYS]) / \
        fund["Adj Close"][-ONE_YEAR_TRADE_DAYS] * 100.0
    one_yr_bench = (benchmark['Adj Close'][-1] - benchmark["Adj Close"][-ONE_YEAR_TRADE_DAYS]) / \
        benchmark["Adj Close"][-ONE_YEAR_TRADE_DAYS] * 100.0
    alpha = one_yr_fund - (risk_free[-1] + beta * (one_yr_bench - risk_free[-1]))
    return alpha