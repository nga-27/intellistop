import numpy as np

from intellistop import IntelliStop
from plot import plot


def run_app():
    """run_app

    Primary application function that runs the standalone process
    """
    print("")
    fund = input("Enter a fund ticker symbol: ").upper()
    print("")

    if len(fund) == 0:
        print("ERROR: No fund ticker entered on input. Exiting...")
        return

    stops = IntelliStop()
    vf_data = stops.run_analysis_for_ticker(fund)
    close = stops.return_data(fund)
    dates = stops.return_data(fund, key='__full__').get('Date', [])

    green_zones = [vf_obj.time_index_list for vf_obj in vf_data.data_sets]
    temp_concat = []
    for array in green_zones:
        temp_concat.extend(array)
    red_zones = []
    red_one = []
    for i in range(len(close)):
        if i not in temp_concat:
            red_one.append(i)
        else:
            if len(red_one) > 0:
                red_zones.append(red_one)
                red_one = []
    if len(red_one) > 0:
        red_zones.append(red_one)

    yellow_zones = []
    for vf_obj in vf_data.data_sets:
        yellow_one = []
        for i, ind in enumerate(vf_obj.time_index_list):
            if close[ind] < vf_obj.caution_line[i]:
                yellow_one.append(ind)
            else:
                if len(yellow_one) > 0:
                    yellow_zones.append(yellow_one)
                    yellow_one = []
    if len(yellow_one) > 0:
        yellow_zones.append(yellow_one)

    min_value = min(
        [
            min([min(vf_obj.stop_loss_line) for vf_obj in vf_data.data_sets]),
            min(close)
        ]
    )
    range_value = max(close) - min_value

    plot_config = plot.set_plot_config(
        f"{fund}_stop_losses.png",
        f"{fund} - Stop Loss Analysis (VF: {np.round(vf_data.vf.curated, 3)})",
        view=True
    )
    plot.app_plot(
        close,
        dates,
        vf_data.data_sets,
        green_zones,
        red_zones,
        yellow_zones,
        range_value,
        min_value,
        config=plot_config
    )


if __name__ == "__main__":
    run_app()