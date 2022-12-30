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


def run_app():
    print("")
    fund = input("Enter a fund ticker symbol: ").upper()
    print("")

    stops = IntelliStop()
    vf_data = stops.run_analysis_for_ticker(fund)
    close = stops.return_data(fund)

    plot_config = set_plot_config(f"{fund}_RT_SL.png", f"{fund} - Real-Time Stop Loss ({np.round(vf_data.vq.curated, 3)})", view=True)
    plot.app_plot([list(range(len(close))), list(range(len(vf_data.stop_loss_data_set)))], [close, vf_data.stop_loss_data_set], config=plot_config)


if __name__ == "__main__":
    run_app()