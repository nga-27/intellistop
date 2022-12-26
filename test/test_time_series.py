from pathlib import Path

import numpy as np

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

def test_ts_1(fund: str = "VTI", use_derived = False):
    config = {
        "momentum_period": 10,
        "momentum_calculator": MomentumCalculation.STANDARD
    }
    stops = IntelliStop(config)
    stops.fetch_extended_time_series(fund)
    data = stops.return_data(fund)
    # data = stops.calculated_time_series_stops()

    x, y, top_5, variances, window, sma_50, lp_dataset = stops.calculated_time_series_stops(use_derived=use_derived)
    # plot.plot_generic(x, y)
    # print(top_5)

    plot_config = set_plot_config(f"{fund}_ts_var_1.png", f"TS {window}-Window: {fund}", dual_axes=True, force_plot_y=True)
    # x_lists = [stops.return_data(fund)['Close'], sma_50]
    x_lists = [lp_dataset, sma_50]
    y_lists = [variances]
    legend = ['Close', 'SMA-50', 'Variance']
    plot.plot_multiple_axes_lists(x_lists, y_lists, config=plot_config, legend=legend)
    # plot_config = set_plot_config(f"{fund}_rval_test_ts_1.png", f"Test Time Series 1 RV: {fund}", dual_axes=True, force_plot_y=True)
    # plot.plot_result(stops.return_data(fund)['Close'], data[1], config=plot_config)

    truthy_vars = []
    falsy_vars = []
    for i, datum in enumerate(data['Close']):
        if datum > sma_50[i]:
            truthy_vars.append(variances[i])
        if datum < sma_50[i]:
            falsy_vars.append(variances[i])

    truthy_mean = np.mean(truthy_vars)
    truthy_fraction = (3.0 * truthy_mean) / np.average(data['Close']) * 100.0
    falsy_mean = np.mean(falsy_vars)
    falsy_fraction = (3.0 * falsy_mean) / np.average(data['Close']) * 100.0
    # print(f"Average of successes: {fund} :: {truthy_mean} ({3.0 * truthy_mean}) ({truthy_mean**2}) [{truthy_fraction}]")
    # print(f"Average of successes: {fund} :: {falsy_mean} ({3.0 * falsy_mean}) ({falsy_mean**2}) [{falsy_fraction}]")

    truthy_sl = max(data['Close']) * (1.0 - (truthy_fraction / 100.0))
    falsy_sl = max(data['Close']) * (1.0 - (falsy_fraction / 100.0))
    print(f"{fund} max: {max(data['Close'])}")
    # print(f"Truthy stop loss: {truthy_sl}")
    # print(f"Falsy stop loss: {falsy_sl}")

    root_sq_mean = np.sqrt((truthy_mean ** 2) + (falsy_mean ** 2))
    root_sq_fraction = (3.0 * root_sq_mean) / np.average(data['Close']) * 100.0
    root_sq_sl = max(data['Close']) * (1.0 - (root_sq_fraction / 100.0))
    print(f"Root Square stop loss: {root_sq_sl} ({root_sq_fraction})")
