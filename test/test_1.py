from intellistop import IntelliStop

def test_2():
    stops = IntelliStop()
    stops.fetch_data("VTI")
    stops.calculate_stops()
