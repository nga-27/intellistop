""" Green/yellow/orange/red zone generating functions """
from typing import List, Tuple

from intellistop import VFStopsResultType


def generate_red_zones(green_zones: List[list], close: list) -> List[list]:
    """generate_red_zones

    Args:
        green_zones (List[list]): assuming everything that has been derived by intellistops
        close (list): list of closing prices

    Returns:
        List[list]: red_zones (list of red zone lists)
    """
    temp_concat = []
    for array in green_zones:
        temp_concat.extend(array)
    red_zones = []
    red_one = []
    for i in range(len(close)):
        if i not in temp_concat:
            if len(red_one) == 0 and i != 0:
                # First one that crosses is still in temp_concat, so we need to go backwards
                red_one.append(i-1)
            red_one.append(i)
        else:
            if len(red_one) > 0:
                red_zones.append(red_one)
                red_one = []
    if len(red_one) > 0:
        red_zones.append(red_one)

    return red_zones


def generate_yellow_orange_zones(vf_data: VFStopsResultType,
                                 close: list) -> Tuple[List[list], List[list]]:
    """generate_yellow_orange_zones

    Args:
        vf_data (VFStopsResultType): volatility factor data from intellistops
        close (list): list of closing prices

    Returns:
        Tuple[List[list], List[list]]: yellow_zones, orange_zones
    """
    yellow_zones = []
    orange_zones = []
    for _, vf_obj in enumerate(vf_data.data_sets):
        yellow_one = []
        orange_one = []
        for i, ind in enumerate(vf_obj.time_index_list):
            if close[ind] < vf_obj.conservative_line[i]:
                orange_one.append(ind)
                if len(yellow_one) > 0:
                    yellow_one.append(ind)
                    yellow_zones.append(yellow_one)
                    yellow_one = []
            elif close[ind] < vf_obj.caution_line[i]:
                yellow_one.append(ind)
                if len(orange_one) > 0:
                    orange_one.append(ind)
                    orange_zones.append(orange_one)
                    orange_one = []
            else:
                if len(yellow_one) > 0:
                    yellow_one.append(ind)
                    yellow_zones.append(yellow_one)
                    yellow_one = []
                if len(orange_one) > 0:
                    orange_one.append(ind)
                    orange_zones.append(orange_one)
                    orange_one = []
        if len(yellow_one) > 0:
            yellow_zones.append(yellow_one)
        if len(orange_one) > 0:
            orange_zones.append(orange_one)

    return yellow_zones, orange_zones
