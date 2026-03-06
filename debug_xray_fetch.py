import requests
import json
import traceback

XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"

def debug_fetch():
    print(f"Fetching {XRAY_URL} in a loop to catch intermittent errors...")
    for i in range(1, 21):
        try:
            print(f"Attempt {i}...", end="", flush=True)
            response = requests.get(XRAY_URL, timeout=10)
            response.raise_for_status()
            
            # Try to parse
            try:
                data = response.json()
                print(" OK.")
            except json.JSONDecodeError as e:
                print("\nJSON Decode Error!")
                print(e)
                print(f"Error at char {e.pos}")
                # Save the bad content
                filename = f"bad_response_{i}.txt"
                with open(filename, "w") as f:
                    f.write(response.text)
                print(f"Saved bad response to {filename}")
                break
                
        except Exception as e:
            print(f"\nRequest failed: {e}")
            traceback.print_exc()
        
        import time
        time.sleep(1)

if __name__ == "__main__":
    debug_fetch()
