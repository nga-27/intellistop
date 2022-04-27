import math
import numpy as np
from scipy.stats import linregress

from intellistop.libs.types import ConfigProperties, KRatioAlgorithms

def get_k_ratio(fund_data: dict, config: ConfigProperties) -> float:
    # may have to convert fund_data to logarithmic
    k_ratio = 0.0
    data_set = fund_data['Adj Close']
    if config.k_ratio_properties.is_log:
        data_set = [math.log(value) for value in fund_data['Adj Close']]

    slope, _, _, _, stderr = linregress(np.linspace(1, len(data_set)+1, len(data_set)), data_set)
    if config.k_ratio_properties.algorithm == KRatioAlgorithms.YR_2013:
        k_ratio = (slope / stderr) * (math.sqrt(config.yf_properties.num_samples_per_calendar_year) / float(len(data_set)))

    if config.k_ratio_properties.algorithm == KRatioAlgorithms.YR_2003:
        k_ratio = (slope / stderr) * (1.0 / float(len(data_set)))

    if config.k_ratio_properties.algorithm == KRatioAlgorithms.YR_1996:
        k_ratio = (slope / stderr) * (1.0 / math.sqrt(float(len(data_set))))

    print(f"k_ratio: {k_ratio}")
    return k_ratio