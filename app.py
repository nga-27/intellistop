""" app.py """
import numpy as np

from intellistop import IntelliStop
from plot import plot
from utils import startup, zone_generator, status


def run_app():
    """run_app

    Primary application function that runs the standalone process
    """
    print("")
    startup.logo_renderer()
    startup.start_header()
    print("")
    fund_raw = input("Enter a fund ticker [or tickers separated by a space]: ").upper()
    print("")

    if len(fund_raw) == 0:
        print("ERROR: No fund ticker entered on input. Exiting...")
        return
    
    fund_stripped = fund_raw.strip()
    fund_list = fund_stripped.split(' ')

    # Can either pass nothing or pass True/False to use_memory for more conservative stops
    stops = IntelliStop(use_memory=True)

    print(f"Starting 'Intellistop' with fund ticker(s): '{fund_raw}'...")

    for fund in fund_list:
        vf_data, has_error = stops.run_analysis_for_ticker(fund)
        if has_error:
            print(f"\r\nFund ticker '{fund}' failed to generate Intellistops data.")
            _ = input("Press any key to continue...")
            continue

        close = stops.return_data(fund)
        dates = stops.return_data(fund, key='__full__').get('Date', [])

        green_zones = [vf_obj.time_index_list for vf_obj in vf_data.data_sets]
        red_zones = zone_generator.generate_red_zones(green_zones, close)

        yellow_zones, orange_zones = zone_generator.generate_yellow_orange_zones(vf_data, close)

        status_string, status_color, shown_stop_loss = status.get_vf_status(fund, vf_data)

        min_value = min(
            [
                min(min(vf_obj.stop_loss_line) for vf_obj in vf_data.data_sets),
                min(close)
            ]
        )
        range_value = max(close) - min_value

        plot_config = plot.set_plot_config(
            f"{fund}_stop_losses.png",
            f"{fund} - Stop Loss Analysis",
            vf_stop_loss_text=shown_stop_loss,
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
            config=plot_config,
            text_str=status_string,
            str_color=status_color,
            orange_zone_x_values=orange_zones
        )


if __name__ == "__main__":
    run_app()
