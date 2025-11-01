from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import json
import os

def get_city_distances():
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # List of Polish cities
    cities = ['Warsaw', 'Krakow', 'Gdansk', 'Poznan', 'Wroclaw', 'Lodz']
    
    # Initialize geocoder
    geolocator = Nominatim(user_agent="my_logistics_app")
    
    # Dictionary to store city coordinates
    city_coords = {}
    
    # Get coordinates for each city
    print("Fetching city coordinates...")
    for city in cities:
        try:
            location = geolocator.geocode(f"{city}, Poland")
            city_coords[city] = (location.latitude, location.longitude)
            print(f"Found coordinates for {city}")
            time.sleep(1)  # Respect API rate limits
        except Exception as e:
            print(f"Error getting coordinates for {city}: {e}")
    
    # Dictionary to store all routes and distances
    routes = {}
    
    # Calculate distances between all city pairs
    print("\nCalculating distances...")
    for origin in cities:
        routes[origin] = {}
        for destination in cities:
            if origin != destination:
                distance = round(geodesic(city_coords[origin], 
                                       city_coords[destination]).kilometers, 2)
                routes[origin][destination] = distance
                print(f"Distance {origin} -> {destination}: {distance} km")
    
    # Save to file with full path
    output_file = os.path.join(data_dir, 'route_distances.txt')
    with open(output_file, 'w') as f:
        json.dump(routes, f, indent=4)
    
    print(f"\nDistances saved to '{output_file}'")
    return routes

if __name__ == "__main__":
    get_city_distances()