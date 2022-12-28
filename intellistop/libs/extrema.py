from enum import Enum


class TrendType(Enum):
    neutral = 'neutral'
    down = 'down'
    up = 'up'


def get_extrema(fund: dict, overcome_pct: float = 0.03, key: str = "Close") -> list:
    extrema_tuples = []
    data = fund[key]

    extrema_tracker = [0, data[0]]
    trend = TrendType.neutral

    for i in range(1, len(data)):
        if trend == TrendType.neutral:
            # Starting out, at least
            if data[i] > extrema_tracker[1] * (1.0 + overcome_pct):
                # Triggered trend up, new "next"
                trend = TrendType.up
                extrema_tracker = [i, data[i]]
                continue

            if data[i] < extrema_tracker[1] * (1.0 - overcome_pct):
                # Triggered trend down, new "next"
                trend = TrendType.down
                extrema_tracker = [i, data[i]]
                continue

        if trend == TrendType.up:
            if data[i] > extrema_tracker[1]:
                extrema_tracker = [i, data[i]]
                continue

            if data[i] < extrema_tracker[1] * (1.0 - overcome_pct):
                # Capture extrema, reset tracker
                extrema_tuples.append((extrema_tracker[0], extrema_tracker[1]))
                extrema_tracker = [i, data[i]]
                trend = TrendType.down
                continue

        if trend == TrendType.down:
            if data[i] < extrema_tracker[1]:
                extrema_tracker = [i, data[i]]
                continue

            if data[i] > extrema_tracker[1] * (1.0 - overcome_pct):
                extrema_tuples.append((extrema_tracker[0], extrema_tracker[1]))
                extrema_tracker = [i, data[i]]
                trend = TrendType.up
                continue

    return extrema_tuples