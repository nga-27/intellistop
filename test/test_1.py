from intellistop import IntelliStop

def test_2():
    print("\r\nStarting test 2...")
    stops = IntelliStop()
    stops.fetch_data("VTI")
    stops.calculate_stops()

def test_3():
    print("\r\nStarting test 3...")
    config = {
        "period": "1y"
    }
    stops = IntelliStop(config)
    stops.fetch_data("VTI")
    stops.calculate_stops()
