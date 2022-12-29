from typing import Tuple, List
import math
import numpy as np

from .lib_types import ConfigProperties, VarianceComponents, StopLossEventLogType, StopLossEventType

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


def get_stop_loss_from_value(price: float, vq: float, isUpFrom: bool = False) -> float:
    if isUpFrom:
        return price * (1.0 + (vq / 100.0))
    return price * (1.0 - (vq / 100.0))


def generate_stop_loss_data_set(data: list,
                                vq: float,
                                smart_moving_average: list,
                                smma_short_slope: list,
                                smma_long_slope: list) -> Tuple[float, List[StopLossEventLogType]]:
    current_stop_losses = []
    stop_loss_logs = []

    current_max = [0, data[0]]
    current_min = [0, 100.0 * data[0]]
    current_stop_losses = [0.0] * len(data)
    current_stop_losses[0] = get_stop_loss_from_value(data[0], vq)
    mode = 'active'
    reset_stop = [False, False, False, False, False]

    for i, price in enumerate(data):
        if mode == 'active':
            if price > current_max[1]:
                current_max[1] = price
                current_max[0] = i
                current_stop_losses[i] = get_stop_loss_from_value(price, vq)
            else:
                # We need to set anyway
                current_stop_losses[i] = current_stop_losses[i-1]

        if price < current_stop_losses[i] and mode == 'active':
            # Officially a STOPPED OUT condition
            mode = 'stopped'
            current_max[1] = 0.0
            log = StopLossEventLogType()
            log.index = i
            log.price = np.round(price, 2)
            stop_loss_logs.append(log)

        if mode == 'stopped':
            # First, track minimum...
            if price < current_min[1]:
                current_min[1] = price
                current_min[0] = i
                log = StopLossEventLogType()
                log.index = i
                log.price = np.round(price, 2)
                log.event = StopLossEventType.minimum
                stop_loss_logs.append(log)

            # Next, price has to rebound 1 VQ % (once)
            if price >= get_stop_loss_from_value(current_min[1], vq, isUpFrom=True) and not reset_stop[0]:
                reset_stop[0] = True

            # Next, price has to be above the SmMA (on-going condition, thus the reset)
            if reset_stop[0] and price > smart_moving_average[i]:
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
                current_max[1] = price
                current_max[0] = i
                current_stop_losses[i] = get_stop_loss_from_value(price, vq)
                log = StopLossEventLogType()
                log.index = i
                log.price = np.round(price, 2)
                log.event = StopLossEventType.activate
                stop_loss_logs.append(log)

    return current_stop_losses, stop_loss_logs
