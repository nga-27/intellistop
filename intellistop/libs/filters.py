import numpy as np
from .lib_types import FilterProperties


def windowed_filter(data: list, props: FilterProperties = {}) -> list:
    windowed_data = [0.0] * len(data)

    for i in range(0, props.filter_half_width):
        windowed_data[i] = data[i]
    for i in range(props.filter_half_width, len(data)-props.filter_half_width-1):
        sub_list = data[i-props.filter_half_width:i+props.filter_half_width+1]
        windowed_data[i] = np.mean(sub_list)
    for i in range(len(data)-props.filter_half_width-1, len(data)):
        windowed_data[i] = data[i]
    return windowed_data


def subtraction_filter(data: list, subtractor: list) -> list:
    if len(subtractor) != len(data):
        return data

    stdev = np.std(data) * 3.0
    subbed_data = [0.0] * len(data)
    for i, datum in enumerate(data):
        subbed_data[i] = (datum - subtractor[i]) / stdev

    return subbed_data


def simple_moving_average_filter(data: list, filter_size: int = 50) -> list:
    filtered = [0.0] * len(data)
    for i in range(0, filter_size - 1):
        filtered[i] = data[i]
    for i in range(filter_size - 1, len(data)):
        filtered[i] = np.average(data[i - (filter_size - 1):i + 1])
    return filtered
    