CAMPUS_NODES = {
    "rv_road_1": (12.924000, 77.500700),
    "rv_road_2": (12.923600, 77.500900),
    "rv_road_3": (12.923200, 77.501100),
    "rv_road_4": (12.922800, 77.501300),
    "rv_road_5": (12.922400, 77.501500),
    
    "north_1": (12.924100, 77.500900),
    "north_2": (12.923900, 77.501100),
    "north_3": (12.923800, 77.501300),
    
    "central_hub_1": (12.923500, 77.500900),
    "central_hub_2": (12.923400, 77.501000),
    "central_hub_3": (12.923300, 77.501200),
    "central_hub_4": (12.923200, 77.500800),
    
    "east_1": (12.923300, 77.501500),
    "east_2": (12.923000, 77.501600),
    "east_3": (12.922700, 77.501700),
    
    "west_1": (12.923600, 77.500600),
    "west_2": (12.923200, 77.500600),
    "west_3": (12.923000, 77.500700),
    "west_4": (12.922700, 77.500800),
    
    "south_1": (12.922500, 77.501200),
    "south_2": (12.922400, 77.501000),
    "south_3": (12.922300, 77.500800),
    "south_4": (12.922600, 77.500600),
    
    "biotech_area": (12.922500, 77.500400),
    "gym_area": (12.922400, 77.500900),
}

CAMPUS_EXITS = {
    "main_gate": (12.924100, 77.500800),
    "pattanagere_metro": (12.924415, 77.498256),
    "south_exit": (12.922200, 77.501600),
    "east_exit": (12.923100, 77.501800),
}


CAMPUS_EDGES = [
    ("rv_road_1", "rv_road_2", 50),
    ("rv_road_2", "rv_road_3", 50),
    ("rv_road_3", "rv_road_4", 50),
    ("rv_road_4", "rv_road_5", 50),
    
    ("north_1", "north_2", 35),
    ("north_2", "north_3", 35),
    ("rv_road_1", "north_1", 25),
    ("rv_road_2", "north_2", 30),
    
    ("central_hub_1", "central_hub_2", 25),
    ("central_hub_2", "central_hub_3", 30),
    ("central_hub_3", "central_hub_4", 30),
    ("central_hub_4", "central_hub_1", 35),
    
    ("rv_road_2", "central_hub_1", 20),
    ("rv_road_3", "central_hub_2", 20),
    ("rv_road_3", "central_hub_3", 25),
    
    ("central_hub_3", "east_1", 25),
    ("east_1", "east_2", 40),
    ("east_2", "east_3", 35),
    ("north_3", "east_1", 30),
    
    ("rv_road_1", "west_1", 20),
    ("rv_road_2", "west_1", 25),
    ("west_1", "west_2", 35),
    ("west_2", "west_3", 30),
    ("west_3", "west_4", 35),
    ("central_hub_4", "west_2", 25),
    
    ("rv_road_4", "south_1", 30),
    ("rv_road_5", "south_2", 25),
    ("south_1", "south_2", 40),
    ("south_2", "south_3", 35),
    ("south_3", "south_4", 40),
    
    ("south_3", "biotech_area", 30),
    ("south_4", "biotech_area", 25),
    ("biotech_area", "gym_area", 35),
    ("south_2", "gym_area", 40),
]


BUILDING_TO_NODE = {
    "Pattanagere Metro Station": "pattanagere_metro",
    "Main Campus Gate": "main_gate",
    "RV Vidyaniketan Post Office": "rv_road_1",
    "Ground Parking": "north_parking",
    "Orchard International School": "main_gate",
    "Bangalore Institute of Management Studies": "pattanagere_metro",
    
    "Innovation Center": "innovation_area",
    "DTL Huddle": "west_2",
    "RVCE Administrative Office": "west_2",
    
    "Old Sports Block": "north_int_1",
    "Medical Centre Hostel": "north_int_2",
    "Telecommunication Department": "north_int_3",
    "New Library": "east_1",
    "Library Annexe": "east_1",
    
    "CS LAB 9 and 10": "central_hub_1",
    "Central Computer Hub": "central_hub_2",
    "Campus Cafeteria": "central_hub_1",
    "Student Activity Center": "central_hub_1",
    "Administration Block": "north_int_2",
    "RV University Main Building": "central_hub_1",
    "Campus Central Plaza": "central_hub_2",
    "Kriakalpa": "central_hub_1",
    
    "A Block": "central_hub_2",
    "B Block": "central_hub_3",
    "C Block": "east_2",
    "Cauvery Block": "north_int_3",
    "Cognitive Centre": "north_int_4",
    "Academic Block 2": "east_2",
    "RVU A Block": "east_2",
    
    "Electrical and Electronics Department": "north_int_4",
    "Electronics and Communication Department": "east_1",
    "Telecommunication Department": "east_1",
    "Aerospace and Information Science": "east_2",
    "Aerospace Workshop": "east_3",
    
    "VRL Bus Depot": "central_hub_3",
    "Diamond Jubli Hostel": "east_1",
    "Chamundi Hostel": "south_int_4",
    "Krishna Hostel": "east_2",
    "Cauvery Block": "north_int_3",
    
    "Mechanical Engineering Block": "west_3",
    "Aircraft Model Display": "west_2",
    "Biotechnology BLOCK": "biotech_area",
    "AIML Biotechnology BLOCK": "south_int_1",
    "AIML BLOCK": "south_int_1",
    "Biotech Quadrangle": "biotech_area",
    "Gymnatorium": "gym_area",
    "Engineering Block": "south_int_2",
    "Science Block": "south_int_3",
}
