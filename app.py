from pathlib import Path

import numpy as np

from intellistop import IntelliStop
from test.utils import plot


PLOT_DIR = Path("output").resolve().mkdir(exist_ok=True)
PLOT_CONFIG = {
    "save_path": "",
    "save_plot": True,
    "has_output": False,
    "title": "",
    "dual_axes": False,
    "force_plot_second_y": False
}

def set_plot_config(file_name: str, title: str, view: bool = False,
                    dual_axes: bool = False, force_plot_y: bool = False) -> dict:
    new_config = PLOT_CONFIG.copy()
    new_config["save_path"] = Path(f"output/{file_name}").resolve()
    new_config["title"] = title
    new_config["dual_axes"] = dual_axes
    new_config["force_plot_second_y"] = force_plot_y
    new_config["save_plot"] = True
    new_config["has_output"] = view
    return new_config


def run_app():
    print("")
    fund = input("Enter a fund ticker symbol: ").upper()
    print("")

    stops = IntelliStop()
    vf_data = stops.run_analysis_for_ticker(fund)
    close = stops.return_data(fund)
    dates = stops.return_data(fund, key='__full__').get('Date', [])

    green_zones = [vf_obj.time_index_list for vf_obj in vf_data.data_sets]
    temp_concat = []
    for array in green_zones:
        temp_concat.extend(array)
    red_zones = []
    red_one = []
    for i in range(len(close)):
        if i not in temp_concat:
            red_one.append(i)
        else:
            if len(red_one) > 0:
                red_zones.append(red_one)
                red_one = []
    if len(red_one) > 0:
        red_zones.append(red_one)

    min_value = min(
        [
            min([min(vf_obj.stop_loss_line) for vf_obj in vf_data.data_sets]),
            min(close)
        ]
    )
    range_value = max(close) - min_value

    plot_config = set_plot_config(f"{fund}_RT_SL.png", f"{fund} - Real-Time Stop Loss ({np.round(vf_data.vq.curated, 3)})", view=True)
    plot.app_plot(
        close,
        dates,
        vf_data.data_sets,
        green_zones,
        red_zones,
        range_value,
        min_value,
        config=plot_config
    )


if __name__ == "__main__":
    run_app()