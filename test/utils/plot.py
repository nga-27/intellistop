from typing import Union, Tuple, List
import datetime

import matplotlib.pyplot as plt
from intellistop import VQTimeSeriesType

# https://matplotlib.org/stable/gallery/color/named_colors.html

COLORS = [
    'black', 'orange', 'blue', 'teal', 'lawngreen', 'fuchsia', 'red', 'gold', 'forestgreen', 'purple'
]

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


def app_plot(prices: list, dates: list, stop_loss_objects: List[VQTimeSeriesType], config: dict = {}, legend: list = []):
    plot_config = PlotConfig(config)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    date_indexes = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    ax.plot(date_indexes, prices, color='black')

    for stop in stop_loss_objects:
        sub_dates = [date_indexes[index] for index in stop.time_index_list]
        ax.plot(sub_dates, stop.caution_line, color='gold')
        ax.plot(sub_dates, stop.stop_loss_line, color='red')

    ax.set_title(plot_config.title)
    ax.legend(legend)

    if plot_config.save_plot:
        plt.savefig(plot_config.save_path)
    if plot_config.has_output:
        plt.show()

    plt.close(fig)