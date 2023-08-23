""" volatility_factor.py

Main "magic" of this tool. Ultimately, the VF is the key. If a price drops below the VF % of the
current max, it is considered to be in a major downward trend, and it should be sold until it
hits its re-entry signal.
"""
from typing import Tuple, List
import numpy as np

from .lib_types import (
    StopLossEventLogType, StopLossEventType, VFTimeSeriesType, VFStopLossResultType
)


def get_stop_loss_from_value(max_price: float,
                             volatility_factor: float,
                             is_up_from: bool = False) -> float:
    """get_stop_loss_from_value

    Given a [recent] max price, return the stop_loss price given the volatility_factor of the
    fund price.

    Args:
        max_price (float): current maximum price
        volatility_factor (float): VF of the fund
        is_up_from (bool, optional): when determining part of the re-entry signal, this is set to
            True. When True, price must exceed this to start the re-entry signal process.
            Defaults to False.

    Returns:
        float: price of the stop loss
    """
    if is_up_from:
        return max_price * (1.0 + (volatility_factor / 100.0))
    return max_price * (1.0 - (volatility_factor / 100.0))


def get_caution_line_from_value(max_price: float, volatility_factor: float) -> float:
    """get_caution_line_from_value

    Caution line is 60% of a drop from the "max_price" to the stop loss price

    Args:
        max_price (float): current maximum price
        volatility_factor (float): VF of the fund

    Returns:
        float: price of the caution line
    """
    return max_price * (1.0 - (0.6 * volatility_factor / 100.0))


def get_current_stop_loss_values(current_vfs: VFStopLossResultType,
                                 current_max: float) -> VFStopLossResultType:
    """get_current_stop_loss_values

    Returns the VFStopLossResultType object, which has fields of aggressive (lowest stop loss
    value), conservative (highest stop loss price), average of both, and curated, which is
    essentially average but also caps the VF at 50.0 for extremely volatile stocks.

    Args:
        current_vfs (VFStopLossResultType): VF object with derived values
        current_max (float): current maximum price

    Returns:
        VFStopLossResultType: aggressive, average, curated, conservative
    """
    current_sl = VFStopLossResultType()
    current_sl.aggressive = get_stop_loss_from_value(current_max, current_vfs.aggressive)
    current_sl.average = get_stop_loss_from_value(current_max, current_vfs.average)
    current_sl.curated = get_stop_loss_from_value(current_max, current_vfs.curated)
    current_sl.conservative = get_stop_loss_from_value(current_max, current_vfs.conservative)

    if current_vfs.curated > 50.0:
        current_sl.curated = get_stop_loss_from_value(current_max, 50.0)
    return current_sl


def generate_stop_loss_data_set(data: list,
                                volatility_factor: float,
                                intelligent_moving_average: list,
                                ima_short_slope: list,
                                ima_long_slope: list,
                                min_vf: float) -> Tuple[
                                    List[VFTimeSeriesType], List[StopLossEventLogType]]:
    """generate_stop_loss_data_set

    The underlying logic function that creates the stop loss curves. This function also generates
    the re-entry signals and restarts the new stop loss automatically.

    Args:
        data (list): [Close or Adjusted] price
        volatility_factor (float): VF of the fund
        intelligent_moving_average (list): data set of the intelligent moving average
        ima_short_slope (list): the short slope of the intelligent moving average
        ima_long_slope (list): the longer moving average of the slope of the intelligent moving
            average

    Returns:
        Tuple[ List[VFTimeSeriesType], List[StopLossEventLogType]]
    """
    # pylint: disable=too-many-branches,too-many-statements
    stop_loss_objects = []
    stop_loss_logs = []

    current_max = [0, data[0]]
    current_min = [0, 100.0 * data[0]]
    mode = 'active'
    reset_stop = [False, False, False, False, False]

    sl_data = VFTimeSeriesType()
    sl_data.caution_line.append(get_caution_line_from_value(data[0], volatility_factor))
    sl_data.max_price = data[0]
    sl_data.max_price_index = 0
    sl_data.stop_loss_line.append(get_stop_loss_from_value(data[0], volatility_factor))
    sl_data.conservative_line.append(get_stop_loss_from_value(data[0], min_vf))
    sl_data.time_index_list.append(0)

    for i in range(1, len(data)):
        if mode == 'active':
            if data[i] > current_max[1]:
                current_max[1] = data[i]
                current_max[0] = i
                sl_data.max_price = data[i]
                sl_data.max_price_index = i
                sl_data.stop_loss_line.append(get_stop_loss_from_value(data[i], volatility_factor))
                sl_data.time_index_list.append(i)
                sl_data.caution_line.append(get_caution_line_from_value(data[i], volatility_factor))
                sl_data.conservative_line.append(get_stop_loss_from_value(data[i], min_vf))
            else:
                # We need to set anyway
                sl_data.caution_line.append(sl_data.caution_line[-1])
                sl_data.stop_loss_line.append(sl_data.stop_loss_line[-1])
                sl_data.conservative_line.append(sl_data.conservative_line[-1])
                sl_data.time_index_list.append(i)

        if mode == 'active' and data[i] < sl_data.stop_loss_line[-1]:
            # Officially a STOPPED OUT condition
            mode = 'stopped'
            current_max[1] = 0.0
            log = StopLossEventLogType()
            log.index = i
            log.price = np.round(data[i], 2)
            stop_loss_logs.append(log)
            stop_loss_objects.append(sl_data)

        if mode == 'stopped':
            # First, track minimum...
            if data[i] < current_min[1]:
                current_min[1] = data[i]
                current_min[0] = i
                log = StopLossEventLogType()
                log.index = i
                log.price = np.round(data[i], 2)
                log.event = StopLossEventType.MINIMUM
                stop_loss_logs.append(log)

            # Next, price has to rebound 1 VF % (once)
            if data[i] >= get_stop_loss_from_value(
                current_min[1], volatility_factor, is_up_from=True) \
                and not reset_stop[0]:
                reset_stop[0] = True

            # Next, price has to be above the IMA (on-going condition, thus the reset)
            if reset_stop[0] and data[i] > intelligent_moving_average[i]:
                reset_stop[1] = True
            else:
                reset_stop[1] = False

            # Next, short-time slope of IMA must be > 0 (on-going)
            if reset_stop[1] and ima_short_slope[i] > 0.0:
                reset_stop[2] = True
            else:
                reset_stop[2] = False

            # Next, long-time slope of IMA must be > 0 (on-going)
            if reset_stop[2] and ima_long_slope[i] > 0.0:
                reset_stop[3] = True
            else:
                reset_stop[3] = True

            # Finally, short_slope > long_slope (on-going)
            if reset_stop[3] and ima_short_slope[i] > ima_long_slope[i]:
                reset_stop[4] = True

            if all(reset_stop):
                # WE DID IT! We're back in!
                mode = 'active'
                reset_stop = [False for _ in reset_stop]
                current_max[1] = data[i]
                current_max[0] = i

                sl_data = VFTimeSeriesType()
                sl_data.stop_loss_line.append(get_stop_loss_from_value(data[i], volatility_factor))
                sl_data.conservative_line.append(get_stop_loss_from_value(data[i], min_vf))
                sl_data.max_price = data[i]
                sl_data.max_price_index = i
                sl_data.time_index_list.append(i)
                sl_data.caution_line.append(get_caution_line_from_value(data[i], volatility_factor))

                log = StopLossEventLogType()
                log.index = i
                log.price = np.round(data[i], 2)
                log.event = StopLossEventType.ACTIVATE
                stop_loss_logs.append(log)

    if mode == 'active':
        # We need to include the stop_loss object at the end if it's still good to go
        stop_loss_objects.append(sl_data)

    return stop_loss_objects, stop_loss_logs
