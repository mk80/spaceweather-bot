import requests
import json
from datetime import datetime

# URL Enpoints
AURORA_URL = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
FORECAST_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"

def fetch_json(url):
    """Fetches JSON data from a URL."""
    try:
        # User-Agent is good practice
        headers = {
            'User-Agent': 'SpaceWeatherBot/1.0 (Discord Bot; contact: admin@example.com)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {url}: {e}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_aurora_data():
    """Fetches the latest aurora forecast."""
    return fetch_json(AURORA_URL)

def get_k_index_data():
    """Fetches the planetary K-index data."""
    return fetch_json(K_INDEX_URL)

def get_forecast_data():
    """Fetches the 3-day K-index forecast."""
    return fetch_json(FORECAST_URL)

def get_xray_data():
    """Fetches the 6-hour GOES X-ray flux data."""
    return fetch_json(XRAY_URL)

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
        
        if kp >= 7:
            level = "Severe" if kp >= 8 else "Strong"
            return {"kp": kp, "time": time_tag, "level": level}
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
    return None

def check_forecast(forecast_data):
    """
    Checks the 3-day forecast for any high K-index predictions.
    We'll alert if Kp >= 7 (Strong Storm) is predicted.
    
    Data format: list of lists
    ["time_tag","kp","observed","noaa_scale"]
    """
    if not forecast_data:
        return None
        
    try:
        # Skip header
        data = forecast_data[1:]
        
        strong_predictions = []
        
        for entry in data:
            # entry: [time, kp, type, scale]
            # e.g., ["2026-02-08 00:00:00","4.67","predicted","G1"]
            time_tag = entry[0]
            kp = float(entry[1])
            prediction_type = entry[2] # "observed", "estimated", "predicted"
            
            # We only care about future predictions, but the file contains recent past too.
            # Simple check: if prediction_type is 'predicted' and kp >= 7
            if prediction_type == "predicted" and kp >= 7:
                strong_predictions.append({"time": time_tag, "kp": kp})
        
        if strong_predictions:
            # Return the highest predicted Kp
            best = max(strong_predictions, key=lambda x: x['kp'])
            return best
            
    except Exception as e:
        print(f"Error parsing forecast data: {e}")
        
    return None

def check_xray_flux(xray_data):
    """
    Checks for high X-ray flux (Radio Blackouts).
    Returns info if Flux >= 1e-5 (R1 Minor).
    """
    if not xray_data:
        return None
    
    try:
        # Filter for the correct energy channel (0.1-0.8nm)
        data = [x for x in xray_data if x.get("energy") == "0.1-0.8nm"]
        if not data:
            return None
        
        # Get the latest reading
        latest = data[-1]
        flux = float(latest['flux'])
        time_tag = latest['time_tag']
        
        # Determine R-Scale
        scale = None
        if flux >= 2e-3:
            scale = "R5 (Extreme)"
        elif flux >= 1e-3:
            scale = "R4 (Severe)"
        elif flux >= 1e-4:
            scale = "R3 (Strong)"
        elif flux >= 5e-5:
            scale = "R2 (Moderate)"
        elif flux >= 1e-5:
            scale = "R1 (Minor)"
            
        if scale:
            return {"flux": flux, "time": time_tag, "scale": scale}
            
    except Exception as e:
        print(f"Error analyzing X-ray data: {e}")
        
    return None
