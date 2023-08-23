""" app.py """
import numpy as np

from intellistop import IntelliStop, CurrentStatusType
from plot import plot
from utils import startup


def run_app():
    """run_app

    Primary application function that runs the standalone process
    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements
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
        temp_concat = []
        for array in green_zones:
            temp_concat.extend(array)
        red_zones = []
        red_one = []
        for i in range(len(close)):
            if i not in temp_concat:
                if len(red_one) == 0 and i != 0:
                    # First one that crosses is still in temp_concat, so we need to go backwards
                    red_one.append(i-1)
                red_one.append(i)
            else:
                if len(red_one) > 0:
                    red_zones.append(red_one)
                    red_one = []
        if len(red_one) > 0:
            red_zones.append(red_one)

        yellow_zones = []
        orange_zones = []
        for _, vf_obj in enumerate(vf_data.data_sets):
            yellow_one = []
            orange_one = []
            for i, ind in enumerate(vf_obj.time_index_list):
                if close[ind] < vf_obj.conservative_line[i]:
                    orange_one.append(ind)
                    if len(yellow_one) > 0:
                        yellow_one.append(ind)
                        yellow_zones.append(yellow_one)
                        yellow_one = []
                elif close[ind] < vf_obj.caution_line[i]:
                    yellow_one.append(ind)
                    if len(orange_one) > 0:
                        orange_one.append(ind)
                        orange_zones.append(orange_one)
                        orange_one = []
                else:
                    if len(yellow_one) > 0:
                        yellow_one.append(ind)
                        yellow_zones.append(yellow_one)
                        yellow_one = []
                    if len(orange_one) > 0:
                        orange_one.append(ind)
                        orange_zones.append(orange_one)
                        orange_one = []
            if len(yellow_one) > 0:
                yellow_zones.append(yellow_one)
            if len(orange_one) > 0:
                orange_zones.append(orange_one)

        min_value = min(
            [
                min(min(vf_obj.stop_loss_line) for vf_obj in vf_data.data_sets),
                min(close)
            ]
        )
        range_value = max(close) - min_value

        status_string = f"{fund} is currently in a green zone. BUY."
        status_color = 'green'
        if vf_data.current_status.status.value == CurrentStatusType.STOPPED_OUT:
            status_string = f"{fund} is currently STOPPED OUT. SELL / wait for a re-entry signal."
            status_color = 'red'
        elif vf_data.current_status.status.value == CurrentStatusType.CAUTION_ZONE:
            status_string = f"{fund} is currently in a caution state. HOLD."
            status_color = 'yellow'
        elif vf_data.current_status.status.value == CurrentStatusType.CONSERVATIVE_OUT:
            status_string = f"{fund} has STOPPED OUT on the conservative factor. SELL / wait for a re-entry signal."
            status_color = 'orange'

        shown_stop_loss = f"VF: {np.round(vf_data.vf.curated, 3)}\n"
        if vf_data.current_status.status.value != 'stopped_out':
            shown_stop_loss += f"Stop Loss: ${np.round(vf_data.stop_loss.curated, 2)}\n"
            shown_stop_loss += f"Cons VF: {np.round(vf_data.vf.historical_cons, 3)}\n"
            shown_stop_loss += f"Cons SL: ${np.round(vf_data.stop_loss.historical_cons, 2)}"
        else:
            shown_stop_loss += "Stop Loss: n/a"

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
