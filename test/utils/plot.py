from typing import Union
import matplotlib.pyplot as plt

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


def plot_generic(x_list: list, y_list: list):
    plt.plot(x_list, y_list)
    plt.show()