import openai
import requests
import os
from geopy.distance import geodesic
import streamlit as st
#from dotenv import load_dotenv

# Load .env file
#load_dotenv()

# Access the API keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENTRIPMAP_API_KEY = st.secrets["OPENTRIPMAP_API_KEY"]
CURRENCY_CONVERSION_RATE = float(st.secrets.get("CURRENCY_CONVERSION_RATE", 83))  # Default to 83 if missing



openai.api_key = OPENAI_API_KEY

# Function to get latitude and longitude of a city
def get_city_coordinates(city):
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENTRIPMAP_API_KEY}"
    response = requests.get(url).json()
    if "lat" in response and "lon" in response:
        return response["lat"], response["lon"]
    return None, None

# Function to fetch tourist attractions
def get_tourist_attractions(city):
    lat, lon = get_city_coordinates(city)
    if not lat or not lon:
        return []

    places_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={lon}&lat={lat}&apikey={OPENTRIPMAP_API_KEY}"
    places_response = requests.get(places_url).json()

    places = []
    for place in places_response.get("features", [])[:20]:  # Limit to 20 places
        name = place["properties"].get("name", "Unknown Place")
        if name:
            places.append(name)

    return places

# Function to estimate travel time based on mode of transport
def estimate_travel_time(distance, mode):
    if mode == "flight":
        return max(distance / 700, 1)  # Approximate flight speed 700 km/h
    elif mode == "train":
        return max(distance / 80, 2)  # Average train speed 80 km/h
    elif mode == "car":
        return max(distance / 60, 2)  # Average car speed 60 km/h
    return None

# Function to generate trip plan
def generate_trip_plan(start_city, destination, budget, days, transport):
    start_lat, start_lon = get_city_coordinates(start_city)
    dest_lat, dest_lon = get_city_coordinates(destination)

    if not start_lat or not start_lon or not dest_lat or not dest_lon:
        return "Invalid city names. Please check and try again."

    distance = geodesic((start_lat, start_lon), (dest_lat, dest_lon)).km
    travel_time = estimate_travel_time(distance, transport)

    # Deduct travel time (only to and from the destination)
    effective_days = days - (travel_time * 2 / 24)
    if effective_days < 1:
        return "Not enough days left after travel. Consider increasing your duration."

    attractions = get_tourist_attractions(destination)
    if not attractions:
        return "Could not fetch attractions. Please try again later."

    # Convert the budget to INR and calculate daily budget in INR
    budget_inr = budget  # Assuming the budget is already in INR
    daily_budget_inr = budget_inr / effective_days
    accommodation = daily_budget_inr * 0.4
    food = daily_budget_inr * 0.3
    travel = daily_budget_inr * 0.2
    misc = daily_budget_inr * 0.1

    itinerary = [f"\nDay 1: Travel from {start_city} to {destination} via {transport} ({distance:.2f} km, {travel_time:.1f} hrs)"]

    attractions_count = len(attractions)
    unique_attractions = set()  # To ensure no duplicates

    for i in range(int(effective_days)):
        # Select unique attraction for each day
        if len(unique_attractions) < attractions_count:
            available_attractions = list(set(attractions) - unique_attractions)
            selected_attraction = available_attractions[i % len(available_attractions)]
            unique_attractions.add(selected_attraction)
        else:
            selected_attraction = attractions[i % attractions_count]

        itinerary.append(f"\nDay {i+2}: Visit {selected_attraction}")

    itinerary.append(f"\nLast Day: Return to {start_city} via {transport} ({travel_time:.1f} hrs)")

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
# print(OPENAI_API_KEY)
# print(OPENTRIPMAP_API_KEY)
# Get user inputs

st.title("AI-Generated Trip Planner")
st.write(OPENAI_API_KEY)
st.write(OPENTRIPMAP_API_KEY)
start_city = st.text_input("Enter your starting city:")
destination = st.text_input("Enter your destination city:")
budget = st.number_input("Enter your total budget (in INR):", min_value=1000.0, step=500.0)
days = st.number_input("How many days will you stay (including travel)?", min_value=1, step=1)
transport = st.selectbox("How will you travel?", ["flight", "train", "car"])

if st.button("Generate Trip Plan"):
    st.write("destination:",destination,"days:",days)
    trip_plan = generate_trip_plan(start_city, destination, budget, days, transport)
    st.write(trip_plan)

# start_city = input("Enter your starting city: ")
# destination = input("Enter your destination city: ")
# budget = float(input("Enter your total budget (in INR): "))
# days = int(input("How many days will you stay (including travel)? "))
# transport = input("How will you travel? (flight, train, car) ").lower()
#
# # Generate and display trip plan
# trip_plan = generate_trip_plan(start_city, destination, budget, days, transport)
# print(trip_plan)
