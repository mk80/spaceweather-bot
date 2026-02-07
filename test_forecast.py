from utils import get_forecast_data, check_forecast
import json

def test_forecast():
    print("Testing Forecast Fetch...")
    data = get_forecast_data()
    if data:
        print("Forecast Data received.")
        # Print a sample
        print(json.dumps(data[:3], indent=2))
        
        # Test check logic
        # Since real data might not have a storm, let's inject a fake one
        print("\nChecking for real predicted storms...")
        alert = check_forecast(data)
        if alert:
             print(f"REAL FORECAST ALERT: {alert}")
        else:
             print("No severe storms predicted in real data.")
             
        # Inject fake data
        print("\nTesting with FAKE severe storm data...")
        fake_data = data[:5] + [["2026-09-01 00:00:00", "8.33", "predicted", "G4"]]
        fake_alert = check_forecast(fake_data)
        if fake_alert:
            print(f"FAKE ALERT DETECTED: {fake_alert}")
        else:
            print("Failed to detect fake alert.")
            
    else:
        print("Failed to fetch Forecast data.")

if __name__ == "__main__":
    test_forecast()
