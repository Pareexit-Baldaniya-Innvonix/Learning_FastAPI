import requests


def test_api():
    url = "http://127.0.0.1:8000"
    print(f"Starting rate limiting test on {url}")

    for i in range(25):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Request {i+1} Allowed: 200 Ok")
            elif response.status_code == 429:
                print(f"Request {i+1} Denied: {response.json().get('detail')}")
            else:
                print(f"Request {i+1}: Error {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Request {i+1}: Failed to connect to server at {url}")
            break


if __name__ == "__main__":
    test_api()
