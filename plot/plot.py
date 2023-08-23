""" plot.py """
from typing import Union, Tuple, List
import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

from intellistop import VFTimeSeriesType


COLORS = [
    'black', 'orange', 'blue', 'teal', 'lawngreen',
    'fuchsia', 'red', 'gold', 'forestgreen', 'purple'
]

Path("output").resolve().mkdir(exist_ok=True)
PLOT_CONFIG = {
    "save_path": "",
    "save_plot": True,
    "has_output": False,
    "title": "",
    "dual_axes": False,
    "force_plot_second_y": False,
    "vf_sl_box_str": ""
}

class PlotConfig:
    """ PlotConfig - Configure Plot saving and titling """
    # pylint: disable=too-few-public-methods
    title: str
    save_plot: bool
    save_path: str
    has_output: bool
    dual_axes: bool
    force_plot_second_y: bool
    vf_sl_box_str: str

    def __init__(self, config: Union[dict, None] = None):
        if not config:
            config = {}
        self.title = config.get('title', "")
        self.save_plot = config.get('save_plot', False)
        self.save_path = config.get('save_path', "output.png")
        self.has_output = config.get('has_output', True)
        self.dual_axes = config.get('dual_axes', False)
        self.force_plot_second_y = config.get('force_plot_second_y', False)
        self.vf_sl_box_str = config.get('vf_sl_box_str', "")


def set_plot_config(file_name: str,
                    title: str,
                    view: bool = False,
                    dual_axes: bool = False,
                    force_plot_y: bool = False,
                    vf_stop_loss_text: str = "") -> dict:
    """set_plot_config

    Args:
        file_name (str): output file to save plot to
        title (str): title of plot
        view (bool, optional): show in real time. Defaults to False.
        dual_axes (bool, optional): for some plots, plot on both y-axes. Defaults to False.
        force_plot_y (bool, optional): for some [deprecated] plot for stop losses.
            Defaults to False.

    Returns:
        dict: plot config object to configure plot
    """
    new_config = PLOT_CONFIG.copy()
    new_config["save_path"] = Path(f"output/{file_name}").resolve()
    new_config["title"] = title
    new_config["dual_axes"] = dual_axes
    new_config["force_plot_second_y"] = force_plot_y
    new_config["save_plot"] = True
    new_config["has_output"] = view
    new_config["vf_sl_box_str"] = vf_stop_loss_text
    return new_config


def plot_result(dataset: list,
                stop_loss: Union[float,list],
                config: dict,
                legend: Union[list, None] = None):
    """plot_result

    Args:
        dataset (list): plotted dataset
        stop_loss (Union[float,list]): single or multiple stop losses
        config (dict): plot config
        legend (Union[list, None], optional): list of plot names. Defaults to None.
    """
    if not legend:
        legend = ['Stop Loss']
    plot_config = PlotConfig(config)
    x_range = list(range(0, len(dataset)))

    fig, ax_handle = plt.subplots()
    ax_handle.plot(x_range, dataset, color='black')

    if isinstance(stop_loss, float):
        stop_loss = [stop_loss]

    if not plot_config.dual_axes:
        if plot_config.force_plot_second_y:
            ax_handle.plot(x_range, stop_loss)
        else:
            for loss in stop_loss:
                stop_range = [loss] * len(dataset)
                ax_handle.plot(x_range, stop_range)

    ax_handle.set_title(plot_config.title)
    legend_extended = ['Close Price']
    legend_extended.extend(legend)
    ax_handle.legend(legend_extended)

    if plot_config.dual_axes:
        ax_handle2 = ax_handle.twinx()
        if plot_config.force_plot_second_y:
            ax_handle2.plot(x_range, stop_loss)
        else:
            for loss in stop_loss:
                stop_range = [loss] * len(dataset)
                ax_handle2.plot(x_range, stop_range)

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()

    plt.close(fig)


def plot_multiple_axes_lists(list_set_a: List[list],
                             list_set_b: List[list],
                             config: dict,
                             legend: Union[list, None] = None):
    """plot_multiple_axes_lists

    Args:
        list_set_a (List[list]): list of lists of one y-axis
        list_set_b (List[list]): list of lists of second y-axis
        config (dict): plot config
        legend (Union[list, None], optional): plot legend list. Defaults to None.
    """
    if not legend:
        legend = []
    plot_config = PlotConfig(config)
    fig, ax_handle = plt.subplots()
    color_counter = 0

    for dataset in list_set_a:
        x_range = list(range(0, len(dataset)))
        ax_handle.plot(x_range, dataset, color=COLORS[color_counter])
        color_counter += 1

    ax_handle2 = ax_handle.twinx()
    for dataset in list_set_b:
        x_range = list(range(0, len(dataset)))
        ax_handle2.plot(x_range, dataset, color=COLORS[color_counter])
        color_counter += 1

    ax_handle.set_title(plot_config.title)
    ax_handle.legend(legend[0:len(list_set_a)])
    ax_handle2.legend(legend[len(list_set_a):len(legend)], loc='upper right')

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()
    plt.close(fig)


def plot_result_bar(dataset: list,
                    x_values: Union[list,None] = None,
                    horizontal_lines: Union[float,None] = None,
                    config: Union[dict, None] = None,
                    legend: Union[list, None] = None):
    """plot_result_bar

    Args:
        dataset (list): data to be plotted
        x_values (Union[list,None], optional): list of x_values. Defaults to None.
        horizontal_lines (Union[float,None], optional): list of horizontal_lines. Defaults to None.
        config (Union[dict, None], optional): plot config. Defaults to None.
        legend (Union[list, None], optional): plot legend. Defaults to None.
    """
    if not config:
        config = {}
    if not legend:
        legend = ['Stop Loss']

    config = PlotConfig(config)
    if x_values is None:
        x_values = range(len(dataset))
    if horizontal_lines is None:
        horizontal_lines = []
    else:
        horizontal_lines = [horizontal_lines] * len(dataset)

    fig, ax_handle = plt.subplots()
    ax_handle.set_title(config.title)
    ax_handle.legend(legend)

    if len(horizontal_lines) > 0:
        ax_handle.plot(x_values, horizontal_lines)
    plt.bar(x_values, dataset)

    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()
    plt.close(fig)


def plot_generic(x_list: list, y_list: list, config: Union[dict, None] = None):
    """plot_generic

    Args:
        x_list (list): x values
        y_list (list): y values
        config (Union[dict, None], optional): plot config. Defaults to None.
    """
    if not config:
        config = {}

    config = PlotConfig(config)
    fig = plt.figure()
    plt.plot(x_list, y_list)
    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()
    plt.close(fig)


def plot_with_circles(dataset: list,
                      list_of_circles: List[Tuple[int, float]],
                      config: Union[dict, None] = None,
                      radius: int = 2):
    """plot_with circles

    Args:
        dataset (list): data to plot
        list_of_circles (List[Tuple[int, float]]): x, y coordinate of circle
        config (Union[dict, None], optional): plot config. Defaults to None.
        radius (int, optional): radius of circles. Defaults to 2.
    """
    if not config:
        config = {}

    config = PlotConfig(config)
    x_range = list(range(0, len(dataset)))

    fig, ax_handle = plt.subplots()
    ax_handle.plot(x_range, dataset, color='black')
    ax_handle.set_title(config.title)

    for coords in list_of_circles:
        target = plt.Circle((coords[0], coords[1]), radius, ec='red')
        plt.gca().add_patch(target)

    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
        plt.show()
    plt.close(fig)


# pylint: disable=too-many-arguments
def app_plot(prices: list, dates: list, stop_loss_objects: List[VFTimeSeriesType],
             green_zone_x_values: List[list], red_zone_x_values: List[list],
             yellow_zone_x_values: List[list], y_range: float, minimum: float,
             config: Union[dict, None] = None, text_str: str = "", str_color: str = "",
             orange_zone_x_values: Union[List[list], None] = None):
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
        text_str (str, optional): text box for notes displayed
        str_color (str, optional): color for notes displayed
        orange_zone_x_values (List[list], optional): list of lists of the orange / conservative zones
    """
    # pylint: disable=too-many-locals
    if not config:
        config = {}
    if not orange_zone_x_values:
        orange_zone_x_values = []

    plot_config = PlotConfig(config)
    fig, ax_handle = plt.subplots()

    date_indexes = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    ax_handle.plot(date_indexes, prices, color='black')

    y_start = minimum - (y_range * 0.05)
    height = y_range * 0.02
    max_index = len(dates)

    for stop in stop_loss_objects:
        sub_dates = [date_indexes[index] for index in stop.time_index_list]
        ax_handle.plot(sub_dates, stop.caution_line, color='gold')
        ax_handle.plot(sub_dates, stop.conservative_line, color='orange')
        ax_handle.plot(sub_dates, stop.stop_loss_line, color='red')

    for green_zone in green_zone_x_values:
        start = mdates.date2num(date_indexes[green_zone[0]])
        end = mdates.date2num(date_indexes[green_zone[-1]])
        width = end - start
        ax_handle.add_patch(
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
        ax_handle.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='red',
                facecolor='red',
                fill=True
            )
        )

    for orange_zone in orange_zone_x_values:
        start = mdates.date2num(date_indexes[orange_zone[0]])
        end = mdates.date2num(date_indexes[orange_zone[-1]])
        width = end - start
        ax_handle.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='orange',
                facecolor='orange',
                fill=True
            )
        )

    for yellow_zone in yellow_zone_x_values:
        start = mdates.date2num(date_indexes[yellow_zone[0]])
        end = mdates.date2num(date_indexes[yellow_zone[-1]])
        width = end - start
        ax_handle.add_patch(
            Rectangle(
                (start, y_start),
                width,
                height,
                edgecolor='yellow',
                facecolor='yellow',
                fill=True
            )
        )

    ax_handle.set_title(plot_config.title)

    if len(text_str) > 0 and len(str_color) > 0:
        new_start = minimum - (y_range * 0.2)
        new_end = minimum + (y_range * 1.02)
        ax_handle.set_ylim(new_start, new_end)
        props = dict(boxstyle='round', facecolor='white', alpha=0.25)
        ax_handle.text(
            0.02,
            0.02,
            text_str,
            color=str_color,
            transform=ax_handle.transAxes,
            bbox=props
        )

    if len(plot_config.vf_sl_box_str) > 0:
        props = dict(boxstyle='round', facecolor='white', alpha=0.25)
        ax_handle.text(
            0.01,
            1.02,
            plot_config.vf_sl_box_str,
            transform=ax_handle.transAxes,
            bbox=props,
            fontsize=8
        )

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()

    plt.close(fig)
