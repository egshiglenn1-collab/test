from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import urllib.request
from urllib.error import URLError, HTTPError

# Updated to your server's IP and port (adjust endpoint path if needed, e.g., "/")
SERVER_URL = "http://192.168.30.10:8000/"
TOTAL_REQUESTS = 30000
MAX_WORKERS = 10  # Number of concurrent requests sent at once


def send_request(request_id):
  try:
    start_time = time.time()
    with urllib.request.urlopen(SERVER_URL, timeout=5) as response:
      status = response.getcode()
      duration = time.time() - start_time
      return {"id": request_id, "status": status, "duration": round(duration, 4)}
  except HTTPError as e:
    return {"id": request_id, "status": e.code, "error": str(e)}
  except URLError as e:
    return {"id": request_id, "status": "Error", "error": str(e.reason)}


def main():
  print(f"Starting {TOTAL_REQUESTS} requests to {SERVER_URL}...")
  start_total = time.time()

  success_count = 0
  error_count = 0

  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [
        executor.submit(send_request, i + 1) for i in range(TOTAL_REQUESTS)
    ]

    for future in as_completed(futures):
      result = future.result()
      # Check if status code is in the 200-299 success range
      if isinstance(result["status"], int) and 200 <= result["status"] < 300:
        success_count += 1
      else:
        error_count += 1
        print(
            f"Request {result['id']} failed: Status {result.get('status')} -"
            f" {result.get('error', 'Unknown error')}"
        )

  total_time = time.time() - start_total
  print("\n--- Summary ---")
  print(f"Total Time: {total_time:.2f} seconds")
  print(f"Successful: {success_count}")
  print(f"Failed: {error_count}")


if __name__ == "__main__":
  main()