from scipy.stats import linregress
import numpy as np
from typing import Union, List

from .types import BetaProperties, BetaPropertyEnum

def get_daily_gains(fund: dict) -> list:
    performance = [0.0] * len(fund['Adj Close'])
    for i in range(1, len(fund['Adj Close'])):
        performance[i] = (fund['Adj Close'][i] - fund['Adj Close'][i-1]) /\
            fund['Adj Close'][i-1]
    return performance


def get_beta(fund: dict, benchmark: dict, properties: dict={}) -> Union[float,List[float]]:
    beta_properties = BetaProperties(properties)
    fund_performance = get_daily_gains(fund)
    bench_performance = get_daily_gains(benchmark)

    if beta_properties.function == BetaPropertyEnum.BETA_ROLLING and beta_properties.shift > 0:
        # Rolling time series case
        num_steps = int(np.floor((len(fund_performance) - beta_properties.window) / beta_properties.shift))
        slopes = list()
        for i in range(0, num_steps * beta_properties.shift, beta_properties.shift):
            end_index = i + beta_properties.window
            slope, _, _, _, _ = linregress(fund_performance[i:end_index], bench_performance[i:end_index])
            slopes.append(slope)
        return slopes

    slope, _, _, _, _ = linregress(fund_performance, bench_performance)
    return slope
