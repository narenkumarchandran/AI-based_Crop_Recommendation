import requests
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import sys
from typing import Optional, Dict, Any
from datetime import datetime

# --- PART 1: SETUP AND PRE-TRAINED MODEL ---
MODEL_FILE = 'crop_recommendation_model.joblib'
DATASET_FILE = 'Crop_recommendation.csv'

def create_dummy_dataset():
    """Creates a dummy dataset if the original is not available."""
    print("Creating dummy dataset for demonstration purposes...")
    
    import numpy as np
    np.random.seed(42)
    
    crops = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 
             'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 
             'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 
             'coconut', 'cotton', 'jute', 'coffee']
    
    n_samples = 2200
    data = []
    
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        
        if crop in ['rice', 'maize']:
            N, P, K = np.random.normal(80, 20), np.random.normal(50, 15), np.random.normal(40, 10)
            temperature, humidity = np.random.normal(25, 5), np.random.normal(80, 10)
            ph, rainfall = np.random.normal(6.5, 0.5), np.random.normal(200, 50)
        else:
            N, P, K = np.random.normal(60, 25), np.random.normal(40, 20), np.random.normal(35, 15)
            temperature, humidity = np.random.normal(22, 8), np.random.normal(65, 15)
            ph, rainfall = np.random.normal(6.8, 0.8), np.random.normal(150, 60)
        
        data.append([
            max(0, N), max(0, P), max(0, K), 
            max(10, temperature), max(20, min(100, humidity)), 
            max(3, min(10, ph)), max(50, rainfall), crop
        ])
    
    df = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    df.to_csv(DATASET_FILE, index=False)
    print(f"Dummy dataset created: {DATASET_FILE}")
    return df

def train_model():
    """Trains and saves the crop recommendation model."""
    print("Training the crop recommendation model...")
    try:
        df = pd.read_csv(DATASET_FILE)
    except (FileNotFoundError, Exception):
        df = create_dummy_dataset()
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved successfully.")
    return model

def load_or_train_model():
    """Loads existing model or trains a new one."""
    if os.path.exists(MODEL_FILE):
        try:
            print("Loading pre-trained crop recommendation model...")
            return joblib.load(MODEL_FILE)
        except Exception as e:
            print(f"Error loading model: {e}. Training new model...")
            return train_model()
    else:
        return train_model()

crop_model = load_or_train_model()

# --- PART 2: LOCATION AND WEATHER API ---
def get_location_from_ip() -> Optional[Dict[str, str]]:
    """Gets user's location using ip-api.com."""
    print("📍 Detecting your location from IP address...")
    try:
        response = requests.get("http://ip-api.com/json/", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return {"state": data.get("regionName", ""), "city": data.get("city", "")}
    except Exception as e:
        print(f"Location detection failed: {e}")
    return None

def get_weather_data(api_key: str, city: str, state: str) -> Dict[str, Any]:
    """Gets weather data using WeatherAPI.com."""
    if not api_key or api_key == "YOUR_WEATHERAPI_KEY":
        print("⚠  WeatherAPI.com key not set. Using default weather data.")
        return {"city": city, "state": state, "temperature": 28.0, "humidity": 65.0}
    
    print(f"🌡  Fetching weather data for {city}, {state}...")
    try:
        params = {"key": api_key, "q": f"{city},{state},India", "aqi": "no"}
        response = requests.get("https://api.weatherapi.com/v1/current.json", params=params, timeout=10)
        response.raise_for_status()
        current = response.json().get("current", {})
        return {
            "city": city, "state": state,
            "temperature": float(current.get("temp_c", 25.0)),
            "humidity": float(current.get("humidity", 60.0))
        }
    except Exception as e:
        print(f"🔴 Error fetching weather data: {e}. Using default values.")
    return {"city": city, "state": state, "temperature": 28.0, "humidity": 65.0}

# --- PART 3: AGMARKNET API (UPDATED) ---
def get_market_data(api_key: str, state: str, district: str, commodity: str, arrival_date: str) -> None:
    """Fetches agricultural market data, generating a URL identical to the user's example."""
    if not api_key or api_key == "YOUR_AGMARKET_API_KEY":
        print("\nWarning: AGMARKNET API key not set. Market price lookup skipped.")
        return

    base_url = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"

    print(f"\n🔍 Searching for '{commodity}' in {district}, {state} on {arrival_date}...")

    # Parameters updated to match the user's provided URL structure
    params = {
        "api-key": api_key,
        "format": "xml",       # CHANGED to xml
        "offset": "5",         # ADDED offset
        "limit": "5",          # CHANGED to 5
        "filters[State]": state.lower(),         # CHANGED to lowercase
        "filters[District]": district.lower(),   # CHANGED to lowercase
        "filters[Commodity]": commodity.lower(), # CHANGED to lowercase
        "filters[Arrival_Date]": arrival_date
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        # This line will print the exact URL requested for verification
        print("Requesting URL:", response.url)
        response.raise_for_status()
        
        # Note: Parsing XML is more complex than JSON. This is a simple check.
        if response.status_code == 200 and len(response.text) > 0:
            print("✅ Successfully received a response from the server.")
            print("   (Displaying results for XML format is not implemented in this example.)")
        else:
            print("❌ No records found or received an empty response.")

    except requests.exceptions.RequestException as e:
        print(f"🔴 Network error: {e}")

# --- PART 4: RECOMMENDATION AND MAIN LOGIC ---
def recommend_crops(weather_data: Dict[str, Any]) -> str:
    """Recommends crops based on live weather and placeholder soil data."""
    try:
        placeholders = {'N': 90.0, 'P': 42.0, 'K': 43.0, 'ph': 6.5, 'rainfall': 202.9}
        input_data = pd.DataFrame([{
            **placeholders,
            'temperature': weather_data['temperature'],
            'humidity': weather_data['humidity']
        }])
        return str(crop_model.predict(input_data)[0])
    except Exception as e:
        print(f"Error in crop recommendation: {e}")
        return "rice"

def safe_input(prompt: str, default: str = "") -> str:
    try:
        return input(prompt).strip() or default
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        sys.exit(0)

def main():
    """Main execution function."""
    print("=" * 50)
    print("        🌾 AI FARMER ASSISTANT 🌾")
    print("=" * 50)
    
    try:
        user_location = get_location_from_ip() or \
            {"state": safe_input("Enter state: ", "Delhi"), "city": safe_input("Enter city: ", "New Delhi")}
        
        # IMPORTANT: Replace with your API keys
        weather_api_key = "4e5616eb1d4743d4b4b203604252309"
        agmarket_api_key = "579b464db66ec23bdd000001f1ce979336e3422966acd01a029a17be"
        
        weather_data = get_weather_data(weather_api_key, user_location['city'], user_location['state'])
        print(f"\n📌 Location: {weather_data['city']}, {weather_data['state']}")
        print(f"🌡  Weather: {weather_data['temperature']}°C, {weather_data['humidity']}% humidity")

        suitable_crop = recommend_crops(weather_data)
        print("\n" + "="*50)
        print(f"✅ RECOMMENDATION: {suitable_crop.upper()}")
        print("="*50)

        print(f"\n💰 Market Price Check")
        commodity = safe_input(f"Enter commodity (default: '{suitable_crop}'): ", suitable_crop)
        default_date = datetime.now().strftime("%d/%m/%y")
        date = safe_input(f"Enter date (DD/MM/YY) [default: {default_date}]: ", default_date)
        
        get_market_data(agmarket_api_key, weather_data['state'], weather_data['city'], commodity, date)
        
        print("\n🌾 Thank you for using AI Farmer Assistant!")
        
    except SystemExit:
        print("\nGoodbye! 🌾")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
main()