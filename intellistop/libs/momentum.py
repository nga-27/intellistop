import pandas as pd

from intellistop.libs.lib_types import ConfigProperties, MomentumCalculation

def calculate_difference_momentum(single_fund_data: dict, properties: ConfigProperties) -> list:
    period = properties.momentum_properties.period
    metric = properties.momentum_properties.metric
    momentum_data = []
    for i in range(0, period):
        momentum_data.append(0.0)
    for i in range(period, len(single_fund_data[metric])):
        momentum_data.append(
            (single_fund_data[metric][i] - single_fund_data[metric][i-period]) / \
                single_fund_data[metric][i-period])
    return momentum_data


def calculate_momentum_standard(single_fund_data: dict, properties: ConfigProperties) -> list:
    period = properties.momentum_properties.period
    metric = properties.momentum_properties.metric
    momentum_data = []
    for i in range(0, period):
        momentum_data.append(1.0)
    for i in range(period, len(single_fund_data[metric])):
        momentum_data.append(single_fund_data[metric][i] / single_fund_data[metric][i-period])
    return momentum_data


def calculate_momentum(single_fund_data: dict, properties: ConfigProperties) -> list:
    calculator = properties.momentum_properties.calculator
    if calculator == MomentumCalculation.STANDARD:
        return calculate_momentum_standard(single_fund_data, properties)
    if calculator == MomentumCalculation.DIFFERENCE:
        return calculate_difference_momentum(single_fund_data, properties)
