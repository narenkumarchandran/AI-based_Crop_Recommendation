import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
import sys

# --- 1. Data Loading and Preparation ---
# Load the crop dataset from a CSV file.
try:
    data = pd.read_csv("Crop_recommendation.csv")
except FileNotFoundError:
    print("ERROR: 'Crop_recommendation.csv' not found. Please make sure the dataset file is in the same directory.")
    sys.exit()

# Create a profile of the ideal conditions for each crop.
crop_means = data.groupby("label").mean(numeric_only=True)

# --- 2. Local Soil Data Integration (Based on Soil Health Dashboard) ---

# Data manually sourced from https://soilhealth.dac.gov.in/nutrient-dashboard
# This is a sample and can be expanded with more states and cities.
STATE_NUTRIENT_STATUS = {
    "Tamil Nadu": {"N": "Low", "P": "Medium", "K": "High"},
    "Karnataka": {"N": "Low", "P": "Low", "K": "High"},
    "Maharashtra": {"N": "Low", "P": "Low", "K": "Very High"},
    "Uttar Pradesh": {"N": "Low", "P": "Medium", "K": "Medium"},
    "Punjab": {"N": "Low", "P": "High", "K": "High"},
    "Andhra Pradesh": {"N": "Low", "P": "Medium", "K": "High"},
    "Kerala": {"N": "Low", "P": "Low", "K": "Medium"},
    "Delhi": {"N": "Medium", "P": "High", "K": "High"}
}

# Representative numerical values for each status category. These are estimations.
NUTRIENT_MAPPING = {
    "Very Low": 10, "Low": 25, "Medium": 50, "High": 75, "Very High": 90
}

# A sample mapping of cities to states. This is not exhaustive.
CITY_TO_STATE_MAP = {
    "chennai": "Tamil Nadu", "coimbatore": "Tamil Nadu", "madurai": "Tamil Nadu", "trichy": "Tamil Nadu",
    "bengaluru": "Karnataka", "mysuru": "Karnataka", "hubli": "Karnataka", "bangalore": "Karnataka",
    "mumbai": "Maharashtra", "pune": "Maharashtra", "nagpur": "Maharashtra",
    "lucknow": "Uttar Pradesh", "kanpur": "Uttar Pradesh", "agra": "Uttar Pradesh",
    "amritsar": "Punjab", "ludhiana": "Punjab",
    "hyderabad": "Andhra Pradesh", "visakhapatnam": "Andhra Pradesh",
    "kochi": "Kerala", "thiruvananthapuram": "Kerala",
    "delhi": "Delhi", "new delhi": "Delhi"
}

def get_soil_data_from_dashboard(city):
    """
    Gets state-level soil nutrient data based on the city provided.
    Data is sourced from the Indian Soil Health Dashboard.
    """
    city_lower = city.lower()
    state = CITY_TO_STATE_MAP.get(city_lower)

    if not state:
        print(f"Warning: City '{city}' not in our database. Using national average soil data from the dataset.")
        # Fallback to dataset average if city/state is unknown
        return {
            "N": data['N'].mean(),
            "P": data['P'].mean(),
            "K": data['K'].mean(),
            "ph": data['ph'].mean()
        }

    print(f"\nFound city '{city}' in {state}. Using state-level soil nutrient data.")
    status = STATE_NUTRIENT_STATUS.get(state)
    
    if not status:
         # Safety net if a state is in the city map but not the nutrient map
         print(f"Warning: No nutrient data for {state}. Using national average.")
         return { "N": data['N'].mean(), "P": data['P'].mean(), "K": data['K'].mean(), "ph": data['ph'].mean() }

    # Convert status ("Low", "Medium") to numerical values
    soil_properties = {
        "N": NUTRIENT_MAPPING.get(status["N"], data['N'].mean()),
        "P": NUTRIENT_MAPPING.get(status["P"], data['P'].mean()),
        "K": NUTRIENT_MAPPING.get(status["K"], data['K'].mean()),
    }

    # The dashboard doesn't provide pH, so we use the dataset average as a fallback.
    ph_fallback = data['ph'].mean()
    print(f"Warning: State-level pH not available. Using dataset average: {ph_fallback:.2f}")
    soil_properties['ph'] = ph_fallback

    return soil_properties

# --- 3. Weather API Function ---

def get_weather(api_key, city):
    """
    Fetches temperature, humidity, and rainfall for a given city
    using the WeatherAPI.com service.
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        r = response.json()
        temp = r['current']['temp_c']
        humidity = r['current']['humidity']
        rainfall = r['current']['precip_mm']
        return temp, humidity, rainfall
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            print("ERROR: Invalid WeatherAPI.com API key.")
        elif err.response.status_code == 400:
            print(f"ERROR: City '{city}' not found.")
        else:
            print(f"ERROR: Could not retrieve weather data. Status code: {err.response.status_code}")
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"ERROR: A network error occurred while fetching weather data: {e}")
        return None, None, None

# --- 4. Core Recommendation Logic ---

def check_crop_suitability(crop, land_conditions):
    ideal = crop_means.loc[crop]
    diff = abs(ideal - land_conditions)
    tolerance = ideal * 0.2
    suitable = (diff < tolerance).all()
    return suitable, diff

def recommend_crops(land_conditions, top_n=3):
    sim = cosine_similarity(crop_means.values, [land_conditions.values]).flatten()
    sim_df = pd.DataFrame({"crop": crop_means.index, "similarity": sim})
    return sim_df.sort_values(by="similarity", ascending=False).head(top_n)

# --- 5. Main System Execution ---

def crop_recommendation_system():
    api_key ="4e5616eb1d4743d4b4b203604252309"
    if not api_key:
        print("API key is required.")
        return
        
    city = input("Enter your city: ")
    crop_name = input("Enter the crop you want to grow: ").strip().lower()

    temp, humidity, rainfall = get_weather(api_key, city)
    if temp is None:
        return
        
    soil = get_soil_data_from_dashboard(city)

    land_conditions = pd.Series({
        "N": soil["N"], "P": soil["P"], "K": soil["K"],
        "temperature": temp, "humidity": humidity, "ph": soil["ph"], "rainfall": rainfall
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