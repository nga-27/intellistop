import numpy as np

from intellistop import IntelliStop
from plot import plot


#################################

def test_ts_1(fund: str = "VTI"):
    stops = IntelliStop()
    vf_data = stops.run_analysis_for_ticker(fund)
    dates = stops.return_data(fund, key='__full__').get('Date', [])
    close = stops.return_data(fund)

    plot_config = plot.set_plot_config(
        f"{fund}_RT_SL.png",
        f"{fund} - Real-Time Stop Loss ({np.round(vf_data.vf.curated, 3)})",
        view=True
    )
    plot.app_plot(close, dates, vf_data.data_sets, config=plot_config)