import requests
import json
import traceback

XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"

def debug_fetch():
    print(f"Fetching {XRAY_URL}...")
    try:
        response = requests.get(XRAY_URL, timeout=10)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        print(f"Encoding: {response.encoding}")
        
        # Try to parse
        try:
            data = response.json()
            print("Successfully parsed JSON.")
            print(f"Item count: {len(data)}")
        except json.JSONDecodeError as e:
            print("JSON Decode Error!")
            print(e)
            print(f"Error at char {e.pos}")
            # Print context around the error
            start = max(0, e.pos - 50)
            end = min(len(response.text), e.pos + 50)
            print(f"Context: {response.text[start:end]!r}")
            
    except Exception as e:
        print(f"Request failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_fetch()
