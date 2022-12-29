import numpy as np


def simple_moving_average_filter(data: list, filter_size: int = 50) -> list:
    filtered = [0.0] * len(data)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    for i in range(filter_size - 1, len(data)):
        filtered[i] = np.average(data[i - (filter_size - 1):i + 1])
    return filtered
    

def exponential_moving_average_filter(data: list, filter_size: int = 50, smoothing_coeff: float = 2.0) -> list:
    filtered = [0.0] * len(data)
    coeff = smoothing_coeff / (float(filter_size) + 1.0)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    filtered[filter_size - 1] = np.average(data[0:filter_size])
    for i in range(filter_size, len(data)):
        filtered[i] = float(data[i]) * coeff + filtered[i-1] * (1.0 - coeff)
    return filtered


def weighted_moving_average_filter(data: list, filter_size: int = 50) -> list:
    filtered = [0.0] * len(data)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    for i in range(filter_size - 1, len(data)):
        sum = 0.0
        sum_div = 0.0
        for j in range(i - (filter_size-1), i+1):
            sum += data[j] * (float(j) + 1.0)
            sum_div += float(j) + 1.0
        filtered[i] = sum / sum_div
    return filtered


def smart_moving_average(data: list, filter_size: int = 50) -> list:
    sma = simple_moving_average_filter(data, filter_size=filter_size)
    ema = exponential_moving_average_filter(data, filter_size=filter_size)
    wma = weighted_moving_average_filter(data, filter_size=filter_size)
    filtered = [(ema[i] + wma[i] + sma[i]) / 3.0 for i in range(len(data))]
    return filtered


def get_slope_of_data_set(data_set: list) -> list:
    slope = [0.0] * len(data_set)
    for i in range(1, len(data_set)):
        slope[i] = data_set[i] - data_set[i-1]
    return slope
