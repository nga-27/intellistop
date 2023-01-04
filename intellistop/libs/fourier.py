""" fourier.py

Derive the fourier spectrum of a dataset
"""
from typing import Tuple

import numpy as np
from scipy.fft import fft, fftfreq


def get_fourier_spectrum(data_set: dict, key: str = 'Close') -> Tuple[np.ndarray, np.ndarray, list]:
    """get_fourier_spectrum

    Get the fourier spectrum of a data set. This is helpful for finding a variance filter size as
    well as filter sizes for moving averages. (A generic or misaligned filter size can cause
    noiser or aliased data that is output from a filter.)

    Args:
        data_set (dict): ticker data set
        key (str, optional): key of the ticker data set to obtain the spectrum. Defaults to 'Close'.

    Returns:
        Tuple[np.ndarray, np.ndarray, list]:
            list of frequencies (x),
            list of power spectra (y),
            list of the top 10 periods (not frequencies) derived in the function
    """
    data_set = data_set[key]
    x_data = range(0, len(data_set))
    y_fft = fft(data_set)
    x_fft = fftfreq(len(x_data), 1.0)[:len(x_data)//2]
    y_spectrum = 2.0 / len(x_data) * np.abs(y_fft[0:len(x_data)//2])

    zipped = list(zip(x_fft, y_spectrum))
    sorted_zip = sorted(zipped, key=lambda x: x[1], reverse=True)
    # Skip the first frequency, as it would be an infinite period
    top_10_periods = [
        1.0 / pair[0] if pair[0] != 0 else len(data_set) * 10.0 for pair in sorted_zip[0:10]]
    return x_fft, y_spectrum, top_10_periods
