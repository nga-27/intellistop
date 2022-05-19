from pathlib import Path
from intellistop import IntelliStop

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

##############################

def test_2():
    print("\r\nStarting test 2...")
    stops = IntelliStop()
    stops.fetch_data("VTI")
    stop_loss = stops.calculate_stops()
    config = set_plot_config("test_2.png", "Test 2: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)

def test_3():
    print("\r\nStarting test 3...")
    config = {
        "period": "1y"
    }
    stops = IntelliStop(config)
    stops.fetch_data("VTI")
    stop_loss = stops.calculate_stops()
    config = set_plot_config("test_3.png", "Test 3: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)

def test_4():
    print("\r\nStarting test 4...")
    config = {
        "period": "2y"
    }
    stops = IntelliStop(config)
    stops.fetch_data("VTI")
    stop_loss = stops.calculate_stops()
    config = set_plot_config("test_4.png", "Test 4: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)
