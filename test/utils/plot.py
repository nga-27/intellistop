from typing import Union
import matplotlib.pyplot as plt

# https://matplotlib.org/stable/gallery/color/named_colors.html

class PlotConfig:
    title = ""
    save_plot = False
    save_path = "output.png"
    has_output = True

    def __init__(self, config={}):
        self.title = config.get('title', "")
        self.save_plot = config.get('save_plot', False)
        self.save_path = config.get('save_path', "output.png")
        self.has_output = config.get('has_output', True)


def plot_result(dataset: list, stop_loss: Union[float,list], config: dict, legend: list = ['Stop Loss']):
    config = PlotConfig(config)
    x_range = list(range(0, len(dataset)))
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_range, dataset, color='black')

    if isinstance(stop_loss, float):
        stop_loss = [stop_loss]
    
    for loss in stop_loss:
        stop_range = [loss] * len(dataset)
        ax.plot(x_range, stop_range)

    ax.set_title(config.title)
    legend_extended = ['Close Price']
    legend_extended.extend(legend)
    ax.legend(legend_extended)

    if config.save_plot:
        plt.savefig(config.save_path)
    if config.has_output:
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