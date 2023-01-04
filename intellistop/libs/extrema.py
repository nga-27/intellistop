""" extrema.py """
from typing import List, Tuple
from enum import Enum


class TrendType(Enum):
    """ TrendType """
    NEUTRAL = 'neutral'
    DOWN = 'down'
    UP = 'up'


def get_extrema(fund: dict,
                overcome_pct: float = 0.03,
                key: str = "Close") -> List[Tuple[int, float, TrendType]]:
    """get_extrema

    Return list of local min/max values given the overcome_pct

    Args:
        fund (dict): ticker data dict
        overcome_pct (float, optional): price needs to overcome this percent to trigger a new
            direction. Defaults to 0.03.
        key (str, optional): key of the ticker data dict. Defaults to "Close".

    Returns:
        List[Tuple[int, float, TrendType]]: extrema points: (index, value, UP/DOWN/NEUTRAL)
    """
    extrema_tuples = []
    data = fund[key]

    extrema_tracker = [0, data[0]]
    trend = TrendType.NEUTRAL

    for i in range(1, len(data)):
        if trend == TrendType.NEUTRAL:
            # Starting out, at least
            if data[i] > extrema_tracker[1] * (1.0 + overcome_pct):
                # Triggered trend up, new "next"
                trend = TrendType.UP
                extrema_tracker = [i, data[i]]
                continue

            if data[i] < extrema_tracker[1] * (1.0 - overcome_pct):
                # Triggered trend down, new "next"
                trend = TrendType.DOWN
                extrema_tracker = [i, data[i]]
                continue

        if trend == TrendType.UP:
            if data[i] > extrema_tracker[1]:
                extrema_tracker = [i, data[i]]
                continue

            if data[i] < extrema_tracker[1] * (1.0 - overcome_pct):
                # Capture extrema, reset tracker
                extrema_tuples.append((extrema_tracker[0], extrema_tracker[1], trend))
                extrema_tracker = [i, data[i]]
                trend = TrendType.DOWN
                continue

        if trend == TrendType.DOWN:
            if data[i] < extrema_tracker[1]:
                extrema_tracker = [i, data[i]]
                continue

            if data[i] > extrema_tracker[1] * (1.0 - overcome_pct):
                extrema_tuples.append((extrema_tracker[0], extrema_tracker[1], trend))
                extrema_tracker = [i, data[i]]
                trend = TrendType.UP
                continue

    return extrema_tuples
