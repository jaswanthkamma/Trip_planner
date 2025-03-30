import streamlit as st
from trip_planner import your_function_name  # Adjust with actual function calls from your trip_planner.py

def run_trip_planner():
    # Your trip planner code can be wrapped inside functions and called here
    st.title("AI-Powered Trip Planner")
    starting_city = st.text_input("Enter your starting city:")
    destination_city = st.text_input("Enter your destination city:")
    total_budget = st.number_input("Enter your total budget:")
    days_stay = st.number_input("How many days will you stay?")
    travel_method = st.selectbox("How will you travel?", ["flight", "train", "car"])

    # Call your trip_planner.py functions here to get results
    if st.button('Generate Itinerary'):
        itinerary = generate_itinerary(starting_city, destination_city, total_budget, days_stay, travel_method)
        st.write(itinerary)  # Display the itinerary

if __name__ == "__main__":
    run_trip_planner()
