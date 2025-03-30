To run the application 
'''sh
  python trip_planner.py
'''

Process Documentation

  Input Collection: I prompt the user to provide essential details like the starting city, destination, budget, trip duration, and transport mode. This information helps generate the personalized trip plan.

  Data Handling: Using APIs like OpenAI and OpenTripMap, I gather information on the distance between cities and tourist attractions around the destination. I fetch these details dynamically to ensure accurate and up-to-date results.

  Itinerary Creation: I calculate effective sightseeing days (excluding travel time), and create a day-by-day itinerary based on the available attractions, ensuring the user gets a variety of top places to visit during their stay.

  Budget Calculation: The total budget is divided by effective sightseeing days to estimate daily costs for accommodation, food, travel, and miscellaneous expenses.

  Response Generation: The model responds with the travel itinerary, budget breakdown, and a detailed description of each day’s activities.




Sample Inputs and Outputs

Sample 1: User Input:

Enter your starting city: delhi
Enter your destination city: paris
Enter your total budget (in INR): 2000000
How many days will you stay (including travel)? 15
How will you travel? (flight, train, car) flight

Model Output:

Your AI-Generated Trip Plan from delhi to paris:
Total Budget: INR 2000000.00
Duration: 15 days (Effective sightseeing days: 13)
Planned Itinerary:
Day 1: Travel from delhi to paris via flight (6700.05 km, 9.5 hrs)
Day 2: Visit Eiffel Tower, Louvre Museum
Day 3: Visit Notre-Dame Cathedral, Musée d'Orsay
Day 4: Visit Sacré-Cœur Basilica, Montmartre
Day 5: Visit Musée Rodin, Musée de l'Orangerie
...
Last Day: Return to delhi via flight (9.5 hrs)

Budget Breakdown (Per Day):
Accommodation: INR 153846.15
Food: INR 115384.62
Travel: INR 76923.08
Miscellaneous: INR 38461.54

Enjoy your trip!


