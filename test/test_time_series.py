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
    if view:
        new_config["save_plot"] = False
        new_config["has_output"] = True
    return new_config

#################################

def test_ts_1(fund: str = "VTI"):
    stops = IntelliStop()
    stops.fetch_extended_time_series(fund)
    close = stops.return_data(fund)
    vq_data = stops.calculate_vq_stops_data()

    smart_moving_avg, slope, slope2 = stops.generate_smart_moving_average()

    plot_config = set_plot_config(f"{fund}_stop_loss.png", f"{fund} - Stop Loss")
    plots = [
        vq_data.stop_loss.average,
        vq_data.stop_loss.aggressive,
        vq_data.stop_loss.conservative,
        vq_data.stop_loss.curated
    ]
    # plot.plot_result(
    #     close,
    #     plots,
    #     plot_config,
    #     legend=[
    #         f"${np.round(vq_data.stop_loss.average, 2)} ({np.round(vq_data.vq.average, 3)})",
    #         f"${np.round(vq_data.stop_loss.aggressive, 2)} ({np.round(vq_data.vq.aggressive, 3)})",
    #         f"${np.round(vq_data.stop_loss.conservative, 2)} ({np.round(vq_data.vq.conservative, 3)})",
    #         f"${np.round(vq_data.stop_loss.curated, 2)} ({np.round(vq_data.vq.curated, 3)})"
    #     ]
    # )

    # plot_config = set_plot_config(f"{fund}_smma_filter.png", f"{fund} - SmMA Filter ({np.round(vq_data.vq.curated, 3)})")
    # plot.plot_multiple_axes_lists([close, smart_moving_avg], [slope, slope2], config=plot_config, legend=["Price", "SmMA"])

    stop_loss_maps = stops.analyze_data_set()
    plot_config = set_plot_config(f"{fund}_RT_SL.png", f"{fund} - Real-Time Stop Loss ({np.round(vq_data.vq.curated, 3)})")
    plot.plot_multiple_axes_lists([close, stop_loss_maps,], [], config=plot_config)