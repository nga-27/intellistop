import numpy as np
from .types import ConfigProperties, MomentumCalculation, VarianceComponents

def calculate_variances(data_set: list, config: ConfigProperties) -> VarianceComponents:
    exported = VarianceComponents()
    exported.total_var = np.var(data_set)
    exported.total_std = np.std(data_set)

    negative_data_set = []
    if config.momentum_properties.calculator == MomentumCalculation.DIFFERENCE:
        negative_data_set = [value for value in data_set if value < 0.0]
    if config.momentum_properties.calculator == MomentumCalculation.STANDARD:
        negative_data_set = [value for value in data_set if value < 1.0]

    exported.negative_var = np.var(negative_data_set)
    exported.negative_std = np.std(negative_data_set)
    return exported