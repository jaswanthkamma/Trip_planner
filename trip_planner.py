import openai
import requests
import os
import streamlit as st
from geopy.distance import geodesic

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
CURRENCY_CONVERSION_RATE = float(os.getenv("CURRENCY_CONVERSION_RATE", 83))  # Default to 83 if not found
openai.api_key = OPENAI_API_KEY

# Function to get latitude and longitude of a city
def get_city_coordinates(city):
    city = city.strip().title()  # Capitalize first letter of each word for better matching
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENTRIPMAP_API_KEY}"
    try:
        response = requests.get(url).json()
        st.write(f"API Response for {city}: {response}")  # Debugging: Show response in Streamlit
        if "lat" in response and "lon" in response:
            return response["lat"], response["lon"]
        else:
            return None, None
    except Exception as e:
        st.error(f"Error fetching coordinates for {city}: {e}")
        return None, None

# Function to fetch tourist attractions
def get_tourist_attractions(city):
    lat, lon = get_city_coordinates(city)
    if not lat or not lon:
        return []
    
    places_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={lon}&lat={lat}&apikey={OPENTRIPMAP_API_KEY}"
    places_response = requests.get(places_url).json()
    
    places = [place["properties"].get("name", "Unknown Place") for place in places_response.get("features", [])[:20]]
    return places

# Function to estimate travel time
def estimate_travel_time(distance, mode):
    if mode == "flight":
        return max(distance / 700, 1)
    elif mode == "train":
        return max(distance / 80, 2)
    elif mode == "car":
        return max(distance / 60, 2)
    return None

# Function to generate trip plan
def generate_trip_plan(start_city, destination, budget, days, transport):
    start_lat, start_lon = get_city_coordinates(start_city)
    dest_lat, dest_lon = get_city_coordinates(destination)

    if not start_lat or not start_lon or not dest_lat or not dest_lon:
        return "Invalid city names. Please check and try again."

    distance = geodesic((start_lat, start_lon), (dest_lat, dest_lon)).km
    travel_time = estimate_travel_time(distance, transport)
    
    effective_days = days - (travel_time * 2 / 24)
    if effective_days < 1:
        return "Not enough days left after travel. Consider increasing your duration."

    attractions = get_tourist_attractions(destination)
    if not attractions:
        return "Could not fetch attractions. Please try again later."
    
    budget_inr = budget  # Assuming INR
    daily_budget_inr = budget_inr / effective_days
    accommodation = daily_budget_inr * 0.4
    food = daily_budget_inr * 0.3
    travel = daily_budget_inr * 0.2
    misc = daily_budget_inr * 0.1

    itinerary = [f"Day 1: Travel from {start_city} to {destination} via {transport} ({distance:.2f} km, {travel_time:.1f} hrs)"]
    unique_attractions = set()
    attractions_count = len(attractions)

    for i in range(int(effective_days)):
        available_attractions = list(set(attractions) - unique_attractions)
        selected_attraction = available_attractions[i % len(available_attractions)] if available_attractions else attractions[i % attractions_count]
        unique_attractions.add(selected_attraction)
        itinerary.append(f"Day {i+2}: Visit {selected_attraction}")

    itinerary.append(f"Last Day: Return to {start_city} via {transport} ({travel_time:.1f} hrs)")
    
    return f"""
Your AI-Generated Trip Plan from {start_city} to {destination}:
Total Budget: INR {budget_inr:.2f}
Duration: {days} days (Effective sightseeing days: {int(effective_days)})
Planned Itinerary:
{chr(10).join(itinerary)}

Budget Breakdown (Per Day):
Accommodation: INR {accommodation:.2f}
Food: INR {food:.2f}
Travel: INR {travel:.2f}
Miscellaneous: INR {misc:.2f}

Enjoy your trip!
"""

# Streamlit UI
st.title("AI-Generated Trip Planner")
start_city = st.text_input("Enter your starting city:")
destination = st.text_input("Enter your destination city:")
budget = st.number_input("Enter your total budget (in INR):", min_value=1000.0, step=500.0)
days = st.number_input("How many days will you stay (including travel)?", min_value=1, step=1)
transport = st.selectbox("How will you travel?", ["flight", "train", "car"])

if st.button("Generate Trip Plan"):
    trip_plan = generate_trip_plan(start_city, destination, budget, days, transport)
    st.write(trip_plan)
