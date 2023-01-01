from typing import Union, Tuple, List
import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

from intellistop import VFTimeSeriesType


COLORS = [
    'black', 'orange', 'blue', 'teal', 'lawngreen', 'fuchsia', 'red', 'gold', 'forestgreen', 'purple'
]

PLOT_DIR = Path("output").resolve().mkdir(exist_ok=True)
PLOT_CONFIG = {
    "save_path": "",
    "save_plot": True,
    "has_output": False,
    "title": "",
    "dual_axes": False,
    "force_plot_second_y": False
}

class PlotConfig:
    title: str
    save_plot: bool
    save_path: str
    has_output: bool
    dual_axes: bool
    force_plot_second_y: bool

    def __init__(self, config={}):
        self.title = config.get('title', "")
        self.save_plot = config.get('save_plot', False)
        self.save_path = config.get('save_path', "output.png")
        self.has_output = config.get('has_output', True)
        self.dual_axes = config.get('dual_axes', False)
        self.force_plot_second_y = config.get('force_plot_second_y', False)


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


def plot_result(dataset: list, stop_loss: Union[float,list], config: dict, legend: list = ['Stop Loss']):
    plot_config = PlotConfig(config)
    x_range = list(range(0, len(dataset)))
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_range, dataset, color='black')

    if isinstance(stop_loss, float):
        stop_loss = [stop_loss]
    
    if not plot_config.dual_axes:
        if plot_config.force_plot_second_y:
            ax.plot(x_range, stop_loss)
        else:
            for loss in stop_loss:
                stop_range = [loss] * len(dataset)
                ax.plot(x_range, stop_range)

    ax.set_title(plot_config.title)
    legend_extended = ['Close Price']
    legend_extended.extend(legend)
    ax.legend(legend_extended)

    if plot_config.dual_axes:
        ax2 = ax.twinx()
        if plot_config.force_plot_second_y:
            ax2.plot(x_range, stop_loss)
        else: 
            for loss in stop_loss:
                stop_range = [loss] * len(dataset)
                ax2.plot(x_range, stop_range)

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()


def plot_multiple_axes_lists(list_set_a: list, list_set_b: list, config: dict, legend: list = []):
    plot_config = PlotConfig(config)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    color_counter = 0

    for dataset in list_set_a:
        x_range = list(range(0, len(dataset)))
        ax.plot(x_range, dataset, color=COLORS[color_counter])
        color_counter += 1

    ax2 = ax.twinx()
    for dataset in list_set_b:
        x_range = list(range(0, len(dataset)))
        ax2.plot(x_range, dataset, color=COLORS[color_counter])
        color_counter += 1

    ax.set_title(plot_config.title)
    ax.legend(legend[0:len(list_set_a)])
    ax2.legend(legend[len(list_set_a):len(legend)], loc='upper right')

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()
    plt.close(fig)


def plot_result_bar(dataset: list, x_values: Union[list,None] = None,
                    horizontal_lines: Union[float,None] = None,
                    config: dict = {}, legend: list = ['Stop Loss']):
    config = PlotConfig(config)
    if x_values is None:
        x_values = range(len(dataset))
    if horizontal_lines is None:
        horizontal_lines = []
    else:
        horizontal_lines = [horizontal_lines] * len(dataset)
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(config.title)
    ax.legend(legend)

    if len(horizontal_lines) > 0:
        ax.plot(x_values, horizontal_lines)
    plt.bar(x_values, dataset)

    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()


def plot_generic(x_list: list, y_list: list, config: dict = {}):
    config = PlotConfig(config)
    fig = plt.figure()
    plt.plot(x_list, y_list)
    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()


def plot_with_circles(dataset: list, list_of_circles: Tuple[int, float], config: dict = {}, radius: int = 2):
    config = PlotConfig(config)
    x_range = list(range(0, len(dataset)))
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_range, dataset, color='black')
    ax.set_title(config.title)

    for coords in list_of_circles:
        target = plt.Circle((coords[0], coords[1]), radius, ec='red')
        plt.gca().add_patch(target)

    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()
    plt.close(fig)


def app_plot(prices: list, dates: list, stop_loss_objects: List[VFTimeSeriesType],
             green_zone_x_values: List[list], red_zone_x_values: List[list],
             yellow_zone_x_values: List[list], y_range: float, minimum: float, config: dict = {}):
    """app_plot

    Primary plotting function that generates the standalone app's visual output. The default is
    that this plot is rendered live as well as stored in output/.

    Args:
        prices (list): close/adjusted close prices
        dates (list): dates of the prices
        stop_loss_objects (List[VFTimeSeriesType]): objects that contain stop losses, caution lines,
        etc.
        green_zone_x_values (List[list]): list of lists of the green / buy zone
        red_zone_x_values (List[list]): list of lists of the red / stopped-out zones
        yellow_zone_x_values (List[list]): list of lists of the yellow / caution zone
        y_range (float): range of max value and min value of data set (includes VFTimeSeriesType)
        minimum (float): minimum of the value of data set (includes VFTimeSeriesType)
        config (dict, optional): plot config options. Defaults to {}.
    """
    plot_config = PlotConfig(config)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    date_indexes = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    ax.plot(date_indexes, prices, color='black')

    y_start = minimum - (y_range * 0.05)
    height = y_range * 0.02

    for stop in stop_loss_objects:
        sub_dates = [date_indexes[index] for index in stop.time_index_list]
        ax.plot(sub_dates, stop.caution_line, color='gold')
        ax.plot(sub_dates, stop.stop_loss_line, color='red')

    for green_zone in green_zone_x_values:
        start = mdates.date2num(date_indexes[green_zone[0]])
        end = mdates.date2num(date_indexes[green_zone[-1]])
        width = end - start
        ax.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='green',
                facecolor='green',
                fill=True
            )
        )

    for red_zone in red_zone_x_values:
        start = mdates.date2num(date_indexes[red_zone[0]])
        end = mdates.date2num(date_indexes[red_zone[-1]])
        width = end - start
        ax.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='red',
                facecolor='red',
                fill=True
            )
        )

    for yellow_zone in yellow_zone_x_values:
        start = mdates.date2num(date_indexes[yellow_zone[0]])
        end = mdates.date2num(date_indexes[yellow_zone[-1]])
        width = end - start
        ax.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='yellow',
                facecolor='yellow',
                fill=True
            )
        )

    ax.set_title(plot_config.title)

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()

    plt.close(fig)