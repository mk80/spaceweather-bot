from utils import get_aurora_data, get_k_index_data, check_northern_us_aurora, check_severe_storm
import json

def test_fetches():
    print("Testing K-Index Fetch...")
    k_data = get_k_index_data()
    if k_data:
        print("K-Index Data received.")
        # Print first few rows to verify structure
        print(json.dumps(k_data[:3], indent=2))
        
        severe = check_severe_storm(k_data)
        if severe:
            print(f"SEVERE STORM DETECTED: {severe}")
        else:
            print("No severe storm currently.")
    else:
        print("Failed to fetch K-Index data.")

    print("\nTesting Aurora Forecast Fetch...")
    aurora_data = get_aurora_data()
    if aurora_data:
        print("Aurora Data received.")
        # Aurora data is large, just check keys
        print(f"Keys: {list(aurora_data.keys())}")
        
        northern_vis = check_northern_us_aurora(aurora_data)
        if northern_vis:
            print(f"AURORA VISIBLE IN NORTHERN US: {northern_vis}")
        else:
            print("Aurora not currently visible in Northern US (normal conditions).")
    else:
        print("Failed to fetch Aurora data.")

if __name__ == "__main__":
    test_fetches()
