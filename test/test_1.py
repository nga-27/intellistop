from intellistop import IntelliStop

def test_1():
    print("")
    stops = IntelliStop()
    data = stops.fetch_data("VTI")
    print(f'{data["VTI"]["Date"][14]} --> {data["VTI"]["Open"][14]}')

def test_2():
    stops = IntelliStop()
    _ = stops.fetch_data("VTI")
    stops.calculate_stops()
