from numpy import var
import math
from .lib_types import ConfigProperties, VarianceComponents

def run_vq_calculation(beta: float, alpha: float, variances: VarianceComponents,
                       k_ratio: float, config: ConfigProperties) -> float:
    print(f"------ {variances.total_std} :: {variances.negative_var} ------")
    vq = (alpha / 100.0 + beta)
    vq = vq ** k_ratio
    vq *= (((variances.total_std * config.vq_properties.std_level) ** 2) - variances.negative_var)
    vq += variances.negative_var
    vq = 3.0 * 100.0 * math.sqrt(vq)

    return vq


def find_latest_max(data_set: list, last_values=100) -> float:
    max_val = 0.0
    for i in range(len(data_set)-1, len(data_set)-last_values, -1):
        if data_set[i] > max_val:
            max_val = data_set[i]
    return max_val