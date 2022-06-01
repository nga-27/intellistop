from typing import Union
import matplotlib.pyplot as plt

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