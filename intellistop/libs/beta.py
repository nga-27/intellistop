from scipy.stats import linregress

def get_daily_gains(fund: dict) -> list:
    performance = [0.0] * len(fund['Adj Close'])
    for i in range(1, len(fund['Adj Close'])):
        performance[i] = (fund['Adj Close'][i] - fund['Adj Close'][i-1]) /\
            fund['Adj Close'][i-1]
    return performance


def get_beta(fund: dict, benchmark: dict, properties: dict={}) -> float:
    fund_performance = get_daily_gains(fund)
    bench_performance = get_daily_gains(benchmark)
    slope, _, r_value, p_value, _ = linregress(fund_performance, bench_performance)
    return slope