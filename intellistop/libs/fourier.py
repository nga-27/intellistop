from typing import Tuple

import numpy as np
from scipy.fft import fft, fftfreq


def get_fourier_spectrum(data_set: dict, key: str = 'Close') -> Tuple[np.ndarray, np.ndarray, list]:
    data_set = data_set[key]
    x = range(0, len(data_set))
    y_fft = fft(data_set)
    x_fft = fftfreq(len(x), 1.0)[:len(x)//2]
    plotable = 2.0 / len(x) * np.abs(y_fft[0:len(x)//2])

    zipped = list(zip(x_fft, plotable))
    sorted_zip = sorted(zipped, key=lambda x: x[1], reverse=True)
    # Skip the first frequency, as it would be an infinite period
    top_10_periods = [1.0 / pair[0] if pair[0] != 0 else len(data_set) * 10.0 for pair in sorted_zip[0:10]]
    return x_fft, plotable, top_10_periods