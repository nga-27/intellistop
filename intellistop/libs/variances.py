import numpy as np
from .types import ConfigProperties, MomentumCalculation, VarianceComponents, VarianceProperties

def calculate_variances(data_set: list, config: ConfigProperties, overrides: dict = {}) -> VarianceComponents:
    exported = VarianceComponents(overrides)

    if exported.variance_type == VarianceProperties.VARIANCE_ROLLING and exported.shift > 0:
        num_steps = int(np.floor((len(data_set) - exported.window) / exported.shift))
        total_vars = list()
        total_stds = list()
        negative_vars = list()
        negative_stds = list()

        for i in range(0, num_steps * exported.shift, exported.shift):
            end_index = i + exported.window
            total_vars.append(np.var(data_set[i:end_index]))
            total_stds.append(np.std(data_set[i:end_index]))

            negative_data_set = []
            overall_mean = np.mean(data_set[i:end_index])
            if config.momentum_properties.calculator == MomentumCalculation.DIFFERENCE:
                negative_data_set = [value for value in data_set[i:end_index] if value < 0.0]
            if config.momentum_properties.calculator == MomentumCalculation.STANDARD:
                negative_data_set = [value for value in data_set[i:end_index] if value < 1.0]
            if exported.variance_type != VarianceProperties.VARIANCE_MOMENTUM:
                negative_data_set = [value for value in data_set[i:end_index] if value < overall_mean]
            negative_vars.append(np.var(negative_data_set))
            negative_stds.append(np.std(negative_data_set))

        exported.total_std = total_stds
        exported.total_var = total_vars
        exported.negative_std = negative_stds
        exported.negative_var = negative_vars
        return exported

    exported.total_var = np.var(data_set)
    exported.total_std = np.std(data_set)
    overall_mean = np.mean(data_set)

    negative_data_set = []
    if config.momentum_properties.calculator == MomentumCalculation.DIFFERENCE:
        negative_data_set = [value for value in data_set if value < 0.0]
    if config.momentum_properties.calculator == MomentumCalculation.STANDARD:
        negative_data_set = [value for value in data_set if value < 1.0]
    if exported.variance_type != VarianceProperties.VARIANCE_MOMENTUM:
        negative_data_set = [value for value in data_set if value < overall_mean]

    exported.negative_var = np.var(negative_data_set)
    exported.negative_std = np.std(negative_data_set)
    return exported