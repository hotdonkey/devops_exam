import requests
import time

url = "https://bbav7reetq7c84fe177c.containers.yandexcloud.net/health"

print("Testing with requests...")
try:
    start = time.time()
    resp = requests.get(url, timeout=10)
    print(f"Success! Status: {resp.status_code}, Time: {time.time() - start:.2f}s")
    print("Response:", resp.json())
except Exception as e:
    print(f"Failed: {e}")