import csv
import random
import math

# Configuration
CENTER_LAT = 12.9716
CENTER_LON = 77.5946
NUM_POIS = 450
FILENAME = "pois.csv"

CATEGORIES = [
    "restaurant", "cafe", "cinema", "hospital", "clinic", 
    "pharmacy", "supermarket", "mall", "atm", "metro_station"
]

def generate_location(lat, lon, radius_km):
    # Random point in circle
    r = radius_km * math.sqrt(random.random())
    theta = random.random() * 2 * math.pi
    
    # 1 degree lat approx 111km
    dlat = (r * math.cos(theta)) / 111.0
    # 1 degree lon approx 111km * cos(lat)
    dlon = (r * math.sin(theta)) / (111.0 * math.cos(math.radians(lat)))
    
    return lat + dlat, lon + dlon

def main():
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "type", "lat", "lon"])
        
        for i in range(1, NUM_POIS + 1):
            category = random.choice(CATEGORIES)
            lat, lon = generate_location(CENTER_LAT, CENTER_LON, 10.0) # 10km radius
            name = f"{category.title()} {i}"
            writer.writerow([i, name, category, round(lat, 6), round(lon, 6)])
            
    print(f"Generated {NUM_POIS} POIs in {FILENAME}")

if __name__ == "__main__":
    main()
