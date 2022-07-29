from pathlib import Path
from intellistop import IntelliStop, MomentumCalculation
from typing import List

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
    stop_loss = stops.calculate_stops().stop_loss
    config = set_plot_config("test_2.png", "Test 2: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)


def test_3():
    print("\r\nStarting test 3...")
    config = {
        "period": "1y"
    }
    stops = IntelliStop(config)
    stops.fetch_data("VTI")
    stop_loss = stops.calculate_stops().stop_loss
    config = set_plot_config("test_3.png", "Test 3: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)


def test_4():
    print("\r\nStarting test 4...")
    config = {
        "period": "2y"
    }
    stops = IntelliStop(config)
    stops.fetch_data("VTI")
    stop_loss = stops.calculate_stops().stop_loss
    config = set_plot_config("test_4.png", "Test 4: VTI")
    plot.plot_result(stops.return_data("VTI")['Close'], stop_loss, config=config)


def test_iterative(ticker: str, target_vq: float) -> list:
    print(f"\r\nStarting iterative test for '{ticker}'...")
    momentum_list = [10, 20, 40]
    period_list = ["1y", "2y"]
    momentum_calc = [MomentumCalculation.STANDARD, MomentumCalculation.DIFFERENCE]
    plot_config = set_plot_config(f"{ticker}_test_iterative.png", f"Test Iterative: {ticker}")
    plot_config2 = set_plot_config(f"{ticker}_test_iterative_dist.png", f"Test Iterative: {ticker}")
    losses = []
    vqs = []
    count = 1
    legend = []
    for calc in momentum_calc:
        for mom in momentum_list:
            for per in period_list:
                config = {
                    "momentum_period": mom,
                    "period": per,
                    "momentum_calculator": calc
                }
                stops = IntelliStop(config)
                stops.fetch_data(ticker)
                result = stops.calculate_stops()
                losses.append(result.stop_loss)
                vqs.append(result.vq)
                count += 1
                legend.append(f"{calc}-{mom}, {per}")
    plot.plot_result(stops.return_data(ticker)['Close'], losses, config=plot_config, legend=legend)
    plot.plot_result_bar(vqs, config=plot_config2, legend=legend, horizontal_lines=target_vq)

    return [vq - target_vq for vq in vqs]


def test_iterative2(ticker: str, target_vq: float) -> list:
    print(f"\r\nStarting iterative test #2 for '{ticker}'...")
    momentum_list = [10, 20, 40]
    start_dates = ["2020-12-31", "2020-04-30"]
    end_date = "2021-12-31"
    momentum_calc = [MomentumCalculation.STANDARD, MomentumCalculation.DIFFERENCE]
    plot_config = set_plot_config(f"{ticker}_test_iterative2.png", f"Test Iterative 2: {ticker}")
    plot_config2 = set_plot_config(f"{ticker}_test_iterative2_dist.png", f"Test Iterative 2: {ticker}")
    losses = []
    vqs = []
    count = 1
    legend = []
    for calc in momentum_calc:
        for mom in momentum_list:
            for per in start_dates:
                config = {
                    "momentum_period": mom,
                    "start_date": per,
                    "end_date": end_date,
                    "momentum_calculator": calc
                }
                stops = IntelliStop(config)
                stops.fetch_data(ticker)
                result = stops.calculate_stops()
                losses.append(result.stop_loss)
                vqs.append(result.vq)
                count += 1
                legend.append(f"{calc}-{mom}, {per}")
    plot.plot_result(stops.return_data(ticker)['Close'], losses, config=plot_config, legend=legend)
    plot.plot_result_bar(vqs, config=plot_config2, legend=legend, horizontal_lines=target_vq)

    return [vq - target_vq for vq in vqs]


def reveal_performance(variances: List[float]) -> list:
    momentum_list = [10, 20, 40]
    start_dates = ["2020-12-31", "2020-04-30"]
    end_date = "2021-12-31"
    momentum_calc = [MomentumCalculation.STANDARD, MomentumCalculation.DIFFERENCE]

    performances = []
    count = 0
    for calc in momentum_calc:
        for mom in momentum_list:
            for per in start_dates:
                performances.append([f"{calc} :: {mom} ::{per} -> {end_date}", variances[count]])
                count += 1
    sorted_list = sorted(performances, key=lambda x: x[1])
    return sorted_list
    