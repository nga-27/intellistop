from pathlib import Path
from intellistop import IntelliStop, MomentumCalculation
from test.utils import plot


PLOT_DIR = Path("output").resolve().mkdir(exist_ok=True)
PLOT_CONFIG = {
    "save_path": "",
    "save_plot": True,
    "has_output": False,
    "title": ""
}

def set_plot_config(file_name: str, title: str, view: bool=False) -> dict:
    new_config = PLOT_CONFIG.copy()
    new_config["save_path"] = Path(f"output/{file_name}").resolve()
    new_config["title"] = title
    if view:
        new_config["save_plot"] = False
        new_config["has_output"] = True
    return new_config

#################################

def test_ts_1():
    config = {
        "momentum_period": 10,
        "momentum_calculator": MomentumCalculation.STANDARD
    }
    stops = IntelliStop(config)
    stops.fetch_extended_time_series("VTI")
    beta = stops.calculated_time_series_stops()
    print(beta)
    config = set_plot_config("test_ts_1.png", "Test Time Series 1: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], beta, config=config)
