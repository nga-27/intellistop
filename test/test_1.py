from intellistop import download_data

def test_1():
    data = download_data("VTI")
    print(f'{data["VTI"]["Date"][14]} --> {data["VTI"]["Open"][14]}')
