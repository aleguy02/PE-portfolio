import requests
import threading

URL = "http://alejandrovillate.duckdns.org:5000/"  # Change to your Flask server URL
NUM_THREADS = 100  # Number of concurrent threads
REQUESTS_PER_THREAD = 100  # Requests per thread


def send_requests():
    for _ in range(REQUESTS_PER_THREAD):
        try:
            requests.get(URL)
        except Exception as e:
            print(f"Request failed: {e}")


threads = []
for _ in range(NUM_THREADS):
    t = threading.Thread(target=send_requests)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Finished sending requests.")
