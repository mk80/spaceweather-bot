import requests
import json
from datetime import datetime

# URL Enpoints
AURORA_URL = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

def fetch_json(url):
    """Fetches JSON data from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_aurora_data():
    """Fetches the latest aurora forecast."""
    return fetch_json(AURORA_URL)

def get_k_index_data():
    """Fetches the planetary K-index data."""
    return fetch_json(K_INDEX_URL)

def check_severe_storm(k_index_data):
    """
    Checks if the K-index is >= 8 (Severe).
    Returns basic info if true, else None.
    Data format for k-index is list of lists: [time_tag, kp, a_running, station_count]
    We want the latest valid entry.
    """
    if not k_index_data:
        return None
    
    # The first item is the header, last item is usually the latest
    # [time_tag, kp, a_running, station_count]
    # Skip header
    try:
        data = k_index_data[1:] 
        if not data:
            return None
            
        latest = data[-1]
        kp = float(latest[1])
        time_tag = latest[0]
        
        if kp >= 8:
            return {"kp": kp, "time": time_tag, "level": "Severe"}
    except (IndexError, ValueError) as e:
        print(f"Error parsing K-index data: {e}")
        
    return None

def check_northern_us_aurora(aurora_data):
    """
    Checks if aurora is likely visible in Northern US.
    Logic: Look for non-zero probability in the relevant latitude/longitude grid.
    
    Northern US approximation:
    Lat: 40 to 50 North
    Long: 235 to 290 East (approx 125W to 70W)
    
    The OVATION data is a list of [Long, Lat, Probability].
    """
    if not aurora_data:
        return None

    # Ovation data structure:
    # "coordinates": [[long, lat, value], ...]
    
    try:
        coordinates = aurora_data.get("coordinates", [])
        max_prob = 0
        
        for long, lat, prob in coordinates:
            # Check if this point is in Northern US rough box
            # Longitudes in the file are 0-360. 
            # US is roughly 235 (West Coast) to 295 (East Coast).
            if 40 <= lat <= 50 and 235 <= long <= 295:
                if prob > max_prob:
                    max_prob = prob
        
        # Threshold: If probability > 50 in this region, it's notable.
        # Normal is usually 0-10 unless there's a storm.
        if max_prob >= 20: # Lowered threshold effectively for "more visible than normal"
             return {"max_prob": max_prob}
             
    except Exception as e:
        print(f"Error analyzing aurora data: {e}")

    return None
