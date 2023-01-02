""" filters.py

Module that houses all applicable filtering and moving average functions
"""
import numpy as np


def simple_moving_average_filter(data: list, filter_size: int = 50) -> list:
    """simple_moving_average_filter

    Args:
        data (list): data array to be filtered
        filter_size (int, optional): size of sma filter in indexes. Defaults to 50.

    Returns:
        list: filtered data
    """
    filtered = [0.0] * len(data)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    for i in range(filter_size - 1, len(data)):
        filtered[i] = np.average(data[i - (filter_size - 1):i + 1])
    return filtered


def exponential_moving_average_filter(data: list,
                                      filter_size: int = 50,
                                      smoothing_coeff: float = 2.0) -> list:
    """exponential_moving_average_filter

    Exponential MA is a tighter-to-signal dataset than the traditional simple moving average.

    Args:
        data (list): data array to be filtered
        filter_size (int, optional): size of ema filter in indexes. Defaults to 50.
        smoothing_coeff (float, optional): ema coefficient, K. Defaults to 2.0.

    Returns:
        list: filtered data
    """
    filtered = [0.0] * len(data)
    coeff = smoothing_coeff / (float(filter_size) + 1.0)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    filtered[filter_size - 1] = np.average(data[0:filter_size])
    for i in range(filter_size, len(data)):
        filtered[i] = float(data[i]) * coeff + filtered[i-1] * (1.0 - coeff)
    return filtered


def weighted_moving_average_filter(data: list, filter_size: int = 50) -> list:
    """weighted_moving_average_filter

    Filter where linearly the most emphasis is on the latest data point

    Args:
        data (list): data array to be filtered
        filter_size (int, optional): size of wma filter in indexes. Defaults to 50.

    Returns:
        list: filtered data
    """
    filtered = [0.0] * len(data)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    for i in range(filter_size - 1, len(data)):
        sum_val = 0.0
        sum_div = 0.0
        for j in range(i - (filter_size-1), i+1):
            sum_val += data[j] * (float(j) + 1.0)
            sum_div += float(j) + 1.0
        filtered[i] = sum_val / sum_div
    return filtered


def smart_moving_average(data: list, filter_size: int = 50) -> list:
    """smart_moving_average

    A filter that takes the combination of simple, exponential, and weighted moving averages
    to generate a deeper moving average that combines traditional, typical market behavior (using
    the simple moving average) with something that reacts more quickly to changes (the
    exponential and weighted moving averages).

    If sized correctly, this should become a major support line for the trend of a price data set.

    Args:
        data (list): data array to be filtered
        filter_size (int, optional): size of the filter. Defaults to 50.

    Returns:
        list: filtered data
    """
    sma = simple_moving_average_filter(data, filter_size=filter_size)
    ema = exponential_moving_average_filter(data, filter_size=filter_size)
    wma = weighted_moving_average_filter(data, filter_size=filter_size)
    filtered = [(ema[i] + wma[i] + sma[i]) / 3.0 for i in range(len(data))]
    return filtered


def get_slope_of_data_set(data_set: list) -> list:
    """get_slope_of_data_set

    A simple differentiation function that returns the change in data from index to index.

    Args:
        data_set (list): data for which to find the slope data set

    Returns:
        list: slope data set of the original data set
    """
    slope = [0.0] * len(data_set)
    for i in range(1, len(data_set)):
        slope[i] = data_set[i] - data_set[i-1]
    return slope
