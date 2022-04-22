from intellistop import IntelliStop

def test_1():
    print("")
    stops = IntelliStop()
    data = stops.fetch_data("VTI")
    print(f'{data["VTI"]["Date"][14]} --> {data["VTI"]["Open"][14]}')
