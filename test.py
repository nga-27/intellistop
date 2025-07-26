""" Test for GHA """
from intellistop import IntelliStop

def run_test() -> bool:
    """ Run the test """
    stops = IntelliStop()
    for ticker_str in ('SPY', 'VTSAX'):
        vf_data, has_error = stops.run_analysis_for_ticker(ticker_str)
        if has_error:
            return False
        if vf_data.fund_name != ticker_str:
            return False
    return True


if __name__ == "__main__":
    assert run_test()
