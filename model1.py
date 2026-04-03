import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
import sys
import time # Import the time module for handling delays

# --- 1. Data Loading and Preparation ---
# Load the crop dataset from a CSV file.
# This dataset contains ideal growing conditions for various crops.
try:
    data = pd.read_csv("Crop_recommendation.csv")
except FileNotFoundError:
    print("ERROR: 'Crop_recommendation.csv' not found. Please make sure the dataset file is in the same directory.")
    sys.exit()

# Group data by crop label and calculate the mean for each condition.
# This creates a profile of the ideal conditions for each crop.
crop_means = data.groupby("label").mean(numeric_only=True)

# --- 2. API Integration Functions ---

# --- Function to get live weather data from WeatherAPI.com ---
def get_weather(api_key, city):
    """
    Fetches temperature, humidity, rainfall, latitude, and longitude for a given city
    using the WeatherAPI.com service.
    """
    # New URL for WeatherAPI.com
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        r = response.json()

        # Updated extraction logic for the new JSON structure
        temp = r['current']['temp_c']
        humidity = r['current']['humidity']
        rainfall = r['current']['precip_mm']  # Precipitation in mm is a good proxy for rainfall
        
        lat = r['location']['lat']
        lon = r['location']['lon']
        
        return temp, humidity, rainfall, lat, lon
        
    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            print("ERROR: Invalid WeatherAPI.com API key. Please check your key and try again.")
        elif response.status_code == 400:
            print(f"ERROR: City '{city}' not found. Please check the spelling.")
        else:
            print(f"ERROR: Could not retrieve weather data. Status code: {response.status_code}")
        return None, None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"ERROR: A network error occurred: {e}")
        return None, None, None, None, None

# --- UPDATED: Function to get soil data from the OpenEPI Soil API ---
def get_soil_data_from_api(lat, lon, 
                           # Using the properties requested by the user
                           properties=["nitrogen", "cec", "phh2o"], 
                           depths=["0-5cm"], 
                           values=["mean"]):
    """
    Fetches soil data from the OpenEPI Soil API (which uses SoilGrids data).
    Includes a retry mechanism for server errors.
    """
    # New API endpoint from the OpenEPI documentation
    url = "https://api.openepi.io/soil/property"
    params = {
        "lon": lon,
        "lat": lat,
        "depths": depths,
        "properties": properties,
        "values": values
    }
    
    print("\nFetching soil data from OpenEPI Soil API...")
    
    max_retries = 3
    delay_seconds = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Will raise an exception for 4xx/5xx errors
            soil_api_data = response.json()

            soil_properties = {}
            # The new API response structure is slightly different.
            layers = soil_api_data.get('properties', [])

            for layer in layers:
                # ADDED SAFETY CHECK: Ensure the 'layer' is a dictionary before processing.
                # This prevents errors if the API returns a null or non-dict item in the list.
                if not isinstance(layer, dict):
                    continue

                name = layer.get('property')
                # Navigate through the new JSON structure
                depth_info = layer.get('layers', [{}])[0]
                value_info = depth_info.get('values', {})
                value = value_info.get('mean')
                
                if value is None:
                    # Use dataset average as a fallback if API returns null
                    fallback_value = data[name].mean() if name in data.columns else 0
                    print(f"Warning: OpenEPI returned no data for '{name}'. Using fallback: {fallback_value:.2f}")
                    soil_properties[name] = fallback_value
                    continue

                # Parse the values based on property name
                if name == 'nitrogen':
                    soil_properties['N'] = value / 100 
                elif name == 'cec': # Using 'cec' as the proxy for Potassium
                    soil_properties['K'] = value
                elif name == 'phh2o':
                    soil_properties['ph'] = value / 10
            
            # --- IMPORTANT FALLBACK FOR PHOSPHORUS ---
            # The OpenEPI soil properties list does not include Phosphorus ('phos').
            # To ensure the recommendation model works, we use the dataset's average as a fallback.
            if 'P' not in soil_properties:
                 p_fallback = data['P'].mean()
                 print(f"Warning: Phosphorus ('P') data not available from this API. Using dataset average: {p_fallback:.2f}")
                 soil_properties['P'] = p_fallback

            # Ensure other core properties needed by the script are present
            for key in ['N', 'K', 'ph']:
                if key not in soil_properties:
                    fallback = data[key].mean()
                    print(f"Warning: Could not determine '{key}'. Using fallback: {fallback:.2f}")
                    soil_properties[key] = fallback
                    
            return soil_properties # Success, return the data

        except requests.exceptions.HTTPError as e:
            if 500 <= e.response.status_code < 600 and attempt < max_retries - 1:
                print(f"Server error ({e.response.status_code}). Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
                delay_seconds *= 2 
            else:
                print(f"ERROR: Could not connect to OpenEPI API after {max_retries} attempts. Error: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: A network error occurred with OpenEPI API: {e}")
            return None

    return None


# --- 3. Core Recommendation Logic (Unchanged) ---

def check_crop_suitability(crop, land_conditions):
    """
    Checks if land conditions are suitable for a given crop within a 20% tolerance.
    """
    ideal = crop_means.loc[crop]
    diff = abs(ideal - land_conditions)
    tolerance = ideal * 0.2
    suitable = (diff < tolerance).all()
    return suitable, diff

def recommend_crops(land_conditions, top_n=3):
    """
    Recommends top N alternative crops based on cosine similarity.
    """
    sim = cosine_similarity(crop_means.values, [land_conditions.values]).flatten()
    sim_df = pd.DataFrame({"crop": crop_means.index, "similarity": sim})
    return sim_df.sort_values(by="similarity", ascending=False).head(top_n)

# --- 4. Main System Execution ---

def crop_recommendation_system():
    """
    Main function to run the crop recommendation system.
    """
    api_key = input("Enter your WeatherAPI.com API key: ")
    if not api_key:
        print("API key is required.")
        return
        
    city = input("Enter your city: ")
    crop_name = input("Enter the crop you want to grow: ").strip().lower()

    temp, humidity, rainfall, lat, lon = get_weather(api_key, city)
    if temp is None:
        return
        
    soil = get_soil_data_from_api(lat, lon)
    if soil is None:
        print("Could not retrieve soil data. Using average dataset values as a fallback.")
        soil = {
            "N": data['N'].mean(),
            "P": data['P'].mean(),
            "K": data['K'].mean(),
            "ph": data['ph'].mean()
        }

    land_conditions = pd.Series({
        "N": soil["N"],
        "P": soil["P"],
        "K": soil["K"],
        "temperature": temp,
        "humidity": humidity,
        "ph": soil["ph"],
        "rainfall": rainfall
    })

    print("\n🌍 Current Land Conditions:")
    print(land_conditions.round(2))

    if crop_name not in crop_means.index:
        print(f"\n❌ Crop '{crop_name}' not found in our dataset.")
        return

    suitable, diff = check_crop_suitability(crop_name, land_conditions)

    if suitable:
        print(f"\n✅ Your land is suitable for cultivating {crop_name.capitalize()}!")
    else:
        print(f"\n⚠ Your land is NOT ideal for {crop_name.capitalize()}. Key differences:")
        unsuitable_conditions = diff[diff > 0.2 * crop_means.loc[crop_name]]
        print(unsuitable_conditions.round(2))

        print("\n🌱 Here are some suggested alternative crops:")
        recs = recommend_crops(land_conditions, top_n=3)
        for _, row in recs.iterrows():
            print(f"- {row['crop'].capitalize()} (Similarity: {row['similarity']:.2f})")

crop_recommendation_system()