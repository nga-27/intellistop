""" variances.py """
from typing import Tuple, Union

import numpy as np


def calculate_time_series_variances(data_set: list,
                                    overrides: Union[dict, None] = None) -> Tuple[list, int]:
    """calculate_time_series variances

    Essentially, find a moving variance across the data_set. This is critical to see how a data set
    changes over time.

    override['window'] acts as a filter for variance size. Default is 50 (when 'use_derived' is
    False) or length of the data_set / 10. This value can also be one of the top 10 periods of a
    data set.

    Args:
        data_set (list): data for which to find the variances
        overrides (Union[dict, None], optional): set of params, such as 'window' and 'use_derived'
            to override defaults. Defaults to None.

    Returns:
        Tuple[list, int]: variances over time, window used in calculation
    """
    if not overrides:
        overrides = {}

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
