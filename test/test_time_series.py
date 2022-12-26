from pathlib import Path
from intellistop import IntelliStop, MomentumCalculation
from intellistop.libs.lib_types import VarianceProperties
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
    config = {
        "momentum_period": 10,
        "momentum_calculator": MomentumCalculation.STANDARD
    }
    stops = IntelliStop(config)
    stops.fetch_extended_time_series(fund)
    data = stops.calculated_time_series_stops()

    plot_config = set_plot_config(f"{fund}_test_ts_1.png", f"Test Time Series 1: {fund}", dual_axes=True, force_plot_y=True)
    plot.plot_result(stops.return_data(fund)['Close'], data[0], config=plot_config)
    plot_config = set_plot_config(f"{fund}_rval_test_ts_1.png", f"Test Time Series 1 RV: {fund}", dual_axes=True, force_plot_y=True)
    plot.plot_result(stops.return_data(fund)['Close'], data[1], config=plot_config)
