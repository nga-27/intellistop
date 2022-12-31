from typing import Tuple

import numpy as np


def calculate_time_series_variances(data_set: list, overrides: dict = {}) -> Tuple[list, int]:
    ts_var = [0.0] * len(data_set)
    window = overrides.get('window', int(max(len(data_set) / 10.0, 50)))
    use_derived = overrides.get('use_derived', False)
    
    if not use_derived:
        window = 50
    mode = overrides.get('mode', 'var')

    if mode == 'var':
        first_var = np.var(data_set[0:window])
        for i in range(window):
            ts_var[i] = first_var
        for i in range(window, len(data_set)):
            ts_var[i] = np.var(data_set[i-window+1:i])

    elif mode == 'std':
        first_var = np.std(data_set[0:window])
        for i in range(window):
            ts_var[i] = first_var
        for i in range(window, len(data_set)):
            ts_var[i] = np.std(data_set[i-window+1:i])

    return ts_var, window