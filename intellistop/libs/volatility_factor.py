from typing import Tuple, List
import math
import numpy as np

from .lib_types import StopLossEventLogType, StopLossEventType, VQTimeSeriesType


def find_latest_max(data_set: list, last_values=100) -> float:
    max_val = 0.0
    for i in range(len(data_set)-1, len(data_set)-last_values, -1):
        if data_set[i] > max_val:
            max_val = data_set[i]
    return max_val


def get_stop_loss_from_list(price_list: list, vq: float) -> Tuple[float, float, int]:
    current_max_value = 0.0
    current_max_index = 0
    current_stop_loss = 0.0
    for i, price in enumerate(price_list):
        if price > current_max_value:
            current_max_value = price
            current_max_index = i
            current_stop_loss = price * (1.0 - (vq / 100.0))

    return current_stop_loss, current_max_value, current_max_index


def get_stop_loss_from_value(max_price: float, vf: float, isUpFrom: bool = False) -> float:
    if isUpFrom:
        return max_price * (1.0 + (vf / 100.0))
    return max_price * (1.0 - (vf / 100.0))


def get_caution_line_from_value(max_price: float, vf: float) -> float:
    return max_price * (1.0 - (0.6 * vf / 100.0))


def generate_stop_loss_data_set(data: list,
                                vf: float,
                                smart_moving_average: list,
                                smma_short_slope: list,
                                smma_long_slope: list) -> Tuple[
                                    List[VQTimeSeriesType], List[StopLossEventLogType]]:
    stop_loss_objects = []
    stop_loss_logs = []

    current_max = [0, data[0]]
    current_min = [0, 100.0 * data[0]]
    mode = 'active'
    reset_stop = [False, False, False, False, False]

    sl_data = VQTimeSeriesType()
    sl_data.caution_line.append(get_caution_line_from_value(data[0], vf))
    sl_data.max_price = data[0]
    sl_data.stop_loss_line.append(get_stop_loss_from_value(data[0], vf))
    sl_data.time_index_list.append(0)

    for i in range(1, len(data)):
        if mode == 'active':
            if data[i] > current_max[1]:
                current_max[1] = data[i]
                current_max[0] = i
                sl_data.max_price = data[i]
                sl_data.stop_loss_line.append(get_stop_loss_from_value(data[i], vf))
                sl_data.time_index_list.append(i)
                sl_data.caution_line.append(get_caution_line_from_value(data[i], vf))
            else:
                # We need to set anyway
                sl_data.caution_line.append(sl_data.caution_line[-1])
                sl_data.stop_loss_line.append(sl_data.stop_loss_line[-1])
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
                log.event = StopLossEventType.minimum
                stop_loss_logs.append(log)

            # Next, price has to rebound 1 VQ % (once)
            if data[i] >= get_stop_loss_from_value(current_min[1], vf, isUpFrom=True) and not reset_stop[0]:
                reset_stop[0] = True

            # Next, price has to be above the SmMA (on-going condition, thus the reset)
            if reset_stop[0] and data[i] > smart_moving_average[i]:
                reset_stop[1] = True
            else:
                reset_stop[1] = False

            # Next, short-time slope of SmMA must be > 0 (on-going)
            if reset_stop[1] and smma_short_slope[i] > 0.0:
                reset_stop[2] = True
            else:
                reset_stop[2] = False

            # Next, long-time slope of SmMA must be > 0 (on-going)
            if reset_stop[2] and smma_long_slope[i] > 0.0:
                reset_stop[3] = True
            else:
                reset_stop[3] = True

            # Finally, short_slope > long_slope (on-going)
            if reset_stop[3] and smma_short_slope[i] > smma_long_slope[i]:
                reset_stop[4] = True

            if all(reset_stop):
                # WE DID IT! We're back in!
                mode = 'active'
                reset_stop = [False for _ in reset_stop]
                current_max[1] = data[i]
                current_max[0] = i
                
                sl_data = VQTimeSeriesType()
                sl_data.stop_loss_line.append(get_stop_loss_from_value(data[i], vf))
                sl_data.max_price = data[i]
                sl_data.time_index_list.append(i)
                sl_data.caution_line.append(get_caution_line_from_value(data[i], vf))

                log = StopLossEventLogType()
                log.index = i
                log.price = np.round(data[i], 2)
                log.event = StopLossEventType.activate
                stop_loss_logs.append(log)

    if mode == 'active':
        # We need to include the stop_loss object at the end if it's still good to go
        stop_loss_objects.append(sl_data)

    return stop_loss_objects, stop_loss_logs
