
import csv

start_id = 959

# Kengeri Area
kengeri_pois = [
    {"name": "Gopalan Arcade Mall", "type": "mall", "lat": 12.935805, "lon": 77.518335},
    {"name": "BGS Gleneagles Global Hospitals", "type": "hospital", "lat": 12.910628, "lon": 77.48655},
    {"name": "Rajarajeshwari Medical College", "type": "college", "lat": 12.8964, "lon": 77.4619},
    {"name": "HK Hospital", "type": "hospital", "lat": 12.9086, "lon": 77.47842},
    {"name": "Shreya Hospital", "type": "hospital", "lat": 12.9150, "lon": 77.4850}, # Approx
]

# Purple Line (East-West)
purple_line = [
    {"name": "Whitefield (Kadugodi) Metro", "type": "station", "lat": 12.9882, "lon": 77.75},
    {"name": "Hopefarm Channasandra Metro", "type": "station", "lat": 12.98793, "lon": 77.75409},
    {"name": "Kadugodi Tree Park Metro", "type": "station", "lat": 12.98565, "lon": 77.7469},
    {"name": "Pattandur Agrahara Metro", "type": "station", "lat": 12.9876, "lon": 77.7382},
    {"name": "Sri Sathya Sai Hospital Metro", "type": "station", "lat": 12.9810, "lon": 77.7276},
    {"name": "Nallurhalli Metro", "type": "station", "lat": 12.9765, "lon": 77.7247},
    {"name": "Kundalahalli Metro", "type": "station", "lat": 12.9774, "lon": 77.7157},
    {"name": "Seetharampalya Metro", "type": "station", "lat": 12.9809, "lon": 77.7088},
    {"name": "Hoodi Metro", "type": "station", "lat": 12.9887, "lon": 77.7112},
    {"name": "Garudacharpalya Metro", "type": "station", "lat": 12.9935, "lon": 77.7037},
    {"name": "Singayyanapalya Metro", "type": "station", "lat": 12.9965, "lon": 77.6927},
    {"name": "KR Pura Metro", "type": "station", "lat": 13.0003, "lon": 77.6766},
    {"name": "Benniganahalli Metro", "type": "station", "lat": 12.9965, "lon": 77.6682},
    {"name": "Baiyappanahalli Metro", "type": "station", "lat": 12.9907, "lon": 77.6524},
    {"name": "Swami Vivekananda Road Metro", "type": "station", "lat": 12.9859, "lon": 77.6449},
    {"name": "Indiranagar Metro", "type": "station", "lat": 12.9718, "lon": 77.6411},
    {"name": "Halasuru Metro", "type": "station", "lat": 12.9765, "lon": 77.6266},
    {"name": "Trinity Metro", "type": "station", "lat": 12.9729, "lon": 77.6170},
    {"name": "MG Road Metro", "type": "station", "lat": 12.9755, "lon": 77.6068},
    {"name": "Cubbon Park Metro", "type": "station", "lat": 12.9810, "lon": 77.5968},
    {"name": "Vidhana Soudha Metro", "type": "station", "lat": 12.9798, "lon": 77.5927},
    {"name": "Sir M Visvesvaraya Metro", "type": "station", "lat": 12.9741, "lon": 77.5840},
    {"name": "Majestic Metro", "type": "station", "lat": 12.9756, "lon": 77.5728},
    {"name": "City Railway Station Metro", "type": "station", "lat": 12.9781, "lon": 77.5696},
    {"name": "Magadi Road Metro", "type": "station", "lat": 12.9755, "lon": 77.5554},
    {"name": "Hosahalli Metro", "type": "station", "lat": 12.9741, "lon": 77.5455},
    {"name": "Vijayanagara Metro", "type": "station", "lat": 12.9708, "lon": 77.5372},
    {"name": "Attiguppe Metro", "type": "station", "lat": 12.9618, "lon": 77.5335},
    {"name": "Deepanjali Nagar Metro", "type": "station", "lat": 12.9587, "lon": 77.5100},
    {"name": "Mysore Road Metro", "type": "station", "lat": 12.9465, "lon": 77.5297},
    {"name": "Nayandahalli Metro", "type": "station", "lat": 12.9468, "lon": 77.5313},
    {"name": "Rajarajeshwari Nagar Metro", "type": "station", "lat": 12.9367, "lon": 77.5195},
    {"name": "Jnanabharathi Metro", "type": "station", "lat": 12.9354, "lon": 77.5124},
    {"name": "Pattanagere Metro", "type": "station", "lat": 12.9150, "lon": 77.4947},
    {"name": "Kengeri Bus Terminal Metro", "type": "station", "lat": 12.9148, "lon": 77.4875},
    {"name": "Kengeri Metro", "type": "station", "lat": 12.9080, "lon": 77.4765},
    {"name": "Challaghatta Metro", "type": "station", "lat": 12.8974, "lon": 77.4612},
]

# Yellow Line (RV Road - Bommasandra)
yellow_line = [
    {"name": "RV Road Metro", "type": "station", "lat": 12.9215, "lon": 77.5802},
    {"name": "Ragigudda Metro", "type": "station", "lat": 12.9170, "lon": 77.5884},
    {"name": "Jayadeva Hospital Metro", "type": "station", "lat": 12.9167, "lon": 77.6001},
    {"name": "BTM Layout Metro", "type": "station", "lat": 12.9165, "lon": 77.6082},
    {"name": "Central Silk Board Metro", "type": "station", "lat": 12.9165, "lon": 77.6205},
    {"name": "Bommanahalli Metro", "type": "station", "lat": 12.9106, "lon": 77.6265},
    {"name": "Hongasandra Metro", "type": "station", "lat": 12.9016, "lon": 77.6320},
    {"name": "Kudlu Gate Metro", "type": "station", "lat": 12.8899, "lon": 77.6392},
    {"name": "Singasandra Metro", "type": "station", "lat": 12.8806, "lon": 77.6449},
    {"name": "Hosa Road Metro", "type": "station", "lat": 12.8707, "lon": 77.6524},
    {"name": "Beratena Agrahara Metro", "type": "station", "lat": 12.8638, "lon": 77.6579},
    {"name": "Electronic City Metro", "type": "station", "lat": 12.8464, "lon": 77.6711},
    {"name": "Infosys Foundation Metro", "type": "station", "lat": 12.8564, "lon": 77.6636},
    {"name": "Huskur Road Metro", "type": "station", "lat": 12.8390, "lon": 77.6775},
    {"name": "Biocon Hebbagodi Metro", "type": "station", "lat": 12.8290, "lon": 77.6813},
    {"name": "Bommasandra Metro", "type": "station", "lat": 12.8105, "lon": 77.7002},
]

# Green Line (Select Major Stations)
green_line = [
    {"name": "Nagasandra Metro", "type": "station", "lat": 13.0485, "lon": 77.5015},
    {"name": "Dasarahalli Metro", "type": "station", "lat": 13.0435, "lon": 77.5126},
    {"name": "Jalahalli Metro", "type": "station", "lat": 13.0371, "lon": 77.5255},
    {"name": "Peenya Metro", "type": "station", "lat": 13.0329, "lon": 77.5338},
    {"name": "Goraguntepalya Metro", "type": "station", "lat": 13.0285, "lon": 77.5408},
    {"name": "Yeshwanthpur Metro", "type": "station", "lat": 13.0238, "lon": 77.5503},
    {"name": "Sandal Soap Factory Metro", "type": "station", "lat": 13.0152, "lon": 77.5539},
    {"name": "Mahalakshmi Metro", "type": "station", "lat": 13.0084, "lon": 77.5557},
    {"name": "Rajajinagar Metro", "type": "station", "lat": 12.9982, "lon": 77.5573},
    {"name": "Kuvempu Road Metro", "type": "station", "lat": 12.9922, "lon": 77.5614},
    {"name": "Srirampura Metro", "type": "station", "lat": 12.9868, "lon": 77.5670},
    {"name": "Mantri Square Sampige Road Metro", "type": "station", "lat": 12.9906, "lon": 77.5709},
    {"name": "Chickpete Metro", "type": "station", "lat": 12.9666, "lon": 77.5746},
    {"name": "KR Market Metro", "type": "station", "lat": 12.9609, "lon": 77.5750},
    {"name": "National College Metro", "type": "station", "lat": 12.9505, "lon": 77.5735},
    {"name": "Lalbagh Metro", "type": "station", "lat": 12.9463, "lon": 77.5801},
    {"name": "South End Circle Metro", "type": "station", "lat": 12.9366, "lon": 77.5828},
    {"name": "Jayanagar Metro", "type": "station", "lat": 12.9304, "lon": 77.5800},
    {"name": "Banashankari Metro", "type": "station", "lat": 12.9155, "lon": 77.5736},
    {"name": "JP Nagar Metro", "type": "station", "lat": 12.9079, "lon": 77.5727},
    {"name": "Yelachenahalli Metro", "type": "station", "lat": 12.8950, "lon": 77.5700},
    {"name": "Konankunte Cross Metro", "type": "station", "lat": 12.8795, "lon": 77.5668},
    {"name": "Doddakallasandra Metro", "type": "station", "lat": 12.8720, "lon": 77.5616},
    {"name": "Vajarahalli Metro", "type": "station", "lat": 12.8625, "lon": 77.5516},
    {"name": "Talaghattapura Metro", "type": "station", "lat": 12.8546, "lon": 77.5435},
    {"name": "Silk Institute Metro", "type": "station", "lat": 12.8447, "lon": 77.5367},
]

all_new = kengeri_pois + purple_line + yellow_line + green_line

filename = "c:/Users/HP/dsaelantigrav/backend/c_core/data/pois.csv"

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    for p in all_new:
        writer.writerow([start_id, p['name'], p['type'], p['lat'], p['lon']])
        start_id += 1

print(f"Added {len(all_new)} new POIs.")
