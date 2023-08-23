from typing import Tuple
import numpy as np
from intellistop import VFStopsResultType, CurrentStatusType


def get_vf_status(fund_name: str, vf_data: VFStopsResultType) -> Tuple[str, str, str]:
    """get_vf_status

    return the string messages to be added as text boxes to plots

    Args:
        fund_name (str): ticker symbol
        vf_data (VFStopsResultType): data structure from intellistops

    Returns:
        Tuple[str, str, str]: status_string, status_color, shown_stop_loss
    """
    status_string = f"{fund_name} is currently in a GREEN zone. BUY."
    status_color = 'green'
    if vf_data.current_status.status.value == CurrentStatusType.STOPPED_OUT.value:
        status_string = f"{fund_name} is currently STOPPED OUT. SELL / wait for a re-entry signal."
        status_color = 'red'
    elif vf_data.current_status.status.value == CurrentStatusType.CAUTION_ZONE.value:
        status_string = f"{fund_name} is currently in a CAUTION state. HOLD."
        status_color = 'yellow'
    elif vf_data.current_status.status.value == CurrentStatusType.CONSERVATIVE_OUT.value:
        status_string = f"{fund_name} has STOPPED OUT on the conservative factor. SELL / wait for a re-entry signal."
        status_color = 'orange'

    shown_stop_loss = f"VF: {np.round(vf_data.vf.curated, 3)}\n"
    if vf_data.current_status.status.value != CurrentStatusType.STOPPED_OUT.value:
        shown_stop_loss += f"Stop Loss: ${np.round(vf_data.stop_loss.curated, 2)}\n"
        shown_stop_loss += f"Cons VF: {np.round(vf_data.vf.historical_cons, 3)}\n"
        shown_stop_loss += f"Cons SL: ${np.round(vf_data.stop_loss.historical_cons, 2)}"
    else:
        shown_stop_loss += "Stop Loss: n/a"

    return status_string, status_color, shown_stop_loss