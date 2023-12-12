import requests
import time

def test_tempi_risposta(endpoint, header):
    try:
        start_time = time.time()
        response = requests.get(endpoint, headers=header)
        elapsed_time = (time.time() - start_time) * 1000

        if response.ok:
            print(f"Tempo di risposta: {elapsed_time:.4f} ms")
        else:
            print(f"Errore: {response.status_code}")

    except requests.RequestException as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    endpoint_url = "http://127.0.0.1:8000/report/user"
    custom_header = {"Authorization": "Bearer <METTERE QUI IL TOKEN>"}

    test_tempi_risposta(endpoint_url, custom_header)

