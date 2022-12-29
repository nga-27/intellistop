from intellistop.libs.lib_types import VarianceProperties
from test import test_1, test_time_series
from test.utils import plot
import numpy as np

# test_1.test_iterative("VTI", 15.35)
# test_1.test_iterative("VGT", 18.35)
# test_1.test_iterative("VHT", 13.92)

# differences = []
# differences.append(test_1.test_iterative2("VTI", 15.35))
# differences.append(test_1.test_iterative2("VTI", 15.35, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y", "filter_half_width": 20}))
# differences.append(test_1.test_iterative2("VGT", 18.35))
# differences.append(test_1.test_iterative2("VGT", 18.35, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y"}))
# differences.append(test_1.test_iterative2("VGT", 18.35, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y", "filter_half_width": 20}))
# differences.append(test_1.test_iterative2("VHT", 13.92))
# differences.append(test_1.test_iterative2("VNQ", 16.81))
# differences.append(test_1.test_iterative2("SPY", 14.44))
# differences.append(test_1.test_iterative2("VO", 15.12))
# differences.append(test_1.test_iterative2("VO", 15.12, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y", "filter_half_width": 20}))
# differences.append(test_1.test_iterative2("AAPL", 27.08))
# differences.append(test_1.test_iterative2("AAPL", 27.08, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_PRICE}))
# differences.append(test_1.test_iterative2("AAPL", 27.08, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y"}))
# differences.append(test_1.test_iterative2("AAPL", 27.08, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_WINDOWED, "period": "1y", "filter_half_width": 2}))
# differences.append(test_1.test_iterative2("AAPL", 27.08, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_MOMENTUM, "period": "1y"}))
# differences.append(test_1.test_iterative2("AAPL", 27.08, config={"start_date": None, "end_date": None, "variance_type": VarianceProperties.VARIANCE_PRICE, "period": "1y"}))
# differences.append(test_1.test_iterative2("K", 16.64, config={"start_date": None, "end_date": None}))

# transposed = [[] for _ in range(len(differences[0]))]
# for diff_row in differences:
#     for i, diff_val in enumerate(diff_row):
#         transposed[i].append(diff_val)

# variances = [np.var(transpo) for transpo in transposed]

# performance = test_1.reveal_performance(variances)
# print("\r\nPerformance:\r\n")
# for perf in performance:
#     print(f"{perf[0]} : {perf[1]}")
# print("")

print("\r\n")

# test_time_series.test_ts_1()
# test_time_series.test_ts_1("VGT")
# test_time_series.test_ts_1("VHT")
test_time_series.test_ts_1("VXUS")
# test_time_series.test_ts_1("VO")
# test_time_series.test_ts_1("VNQ")
# test_time_series.test_ts_1("SPY")
# test_time_series.test_ts_1("WM")


# test_time_series.test_ts_1("AAPL")
# test_time_series.test_ts_1("VCR")
# test_time_series.test_ts_1("TSLA")
test_time_series.test_ts_1("VWINX")
# test_time_series.test_ts_1("MMM")
# test_time_series.test_ts_1("HD")
# test_time_series.test_ts_1("MCD")