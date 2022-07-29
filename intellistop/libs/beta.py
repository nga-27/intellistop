from scipy.stats import linregress
import numpy as np
from typing import Union, List, Tuple

from .types import BetaProperties, BetaPropertyEnum

def get_daily_gains(fund: dict) -> list:
    performance = [0.0] * len(fund['Adj Close'])
    for i in range(1, len(fund['Adj Close'])):
        performance[i] = (fund['Adj Close'][i] - fund['Adj Close'][i-1]) /\
            fund['Adj Close'][i-1]
    return performance


def get_beta(fund: dict, benchmark: dict, properties: dict={}) -> Union[Tuple[float,float],Tuple[List[float],List[float]]]:
    beta_properties = BetaProperties(properties)
    fund_performance = get_daily_gains(fund)
    bench_performance = get_daily_gains(benchmark)

    if beta_properties.function == BetaPropertyEnum.BETA_ROLLING and beta_properties.shift > 0:
        # Rolling time series case
        num_steps = int(np.floor((len(fund_performance) - beta_properties.window) / beta_properties.shift))
        slopes = list()
        r_values = list()
        for i in range(0, num_steps * beta_properties.shift, beta_properties.shift):
            end_index = i + beta_properties.window
            slope, _, r_value, _, _ = linregress(bench_performance[i:end_index], fund_performance[i:end_index])
            slopes.append(slope)
            r_values.append(r_value)

        if beta_properties.match_length:
            slopes2 = [slopes[0]] * beta_properties.window
            r_values2 = [r_values[0]] * beta_properties.window
            for slope in slopes:
                slopes2.extend([slope] * beta_properties.shift)
            for r_val in r_values:
                r_values2.extend([r_val] * beta_properties.shift)
            while len(slopes2) < len(fund_performance):
                slopes2.append(slopes[-1])
                r_values2.append(r_values[-1])
            slopes = slopes2
            r_values = r_values2
        return (slopes, r_values)

    slope, _, r_value, _, _ = linregress(bench_performance, fund_performance)
    return (slope, r_value)
