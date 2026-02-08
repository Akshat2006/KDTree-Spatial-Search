CAMPUS_NODES = {
    # Main North-South Road (RV Road / Bangalore-Mysore Road side)
    "rv_road_north": (12.9242, 77.5008),
    "rv_road_1": (12.9240, 77.5007),
    "rv_road_2": (12.9238, 77.5008),
    "rv_road_3": (12.9236, 77.5009),
    "rv_road_4": (12.9234, 77.5010),
    "rv_road_5": (12.9232, 77.5011),
    "rv_road_6": (12.9230, 77.5012),
    "rv_road_7": (12.9228, 77.5013),
    "rv_road_south": (12.9226, 77.5014),
    
    # East-West Road 1 (Northern)
    "ew_north_1": (12.9241, 77.5010),
    "ew_north_2": (12.9241, 77.5012),
    "ew_north_3": (12.9241, 77.5014),
    "ew_north_4": (12.9241, 77.5016),
    
    # East-West Road 2 (Central Upper)
    "ew_central_1": (12.9236, 77.5008),
    "ew_central_2": (12.9236, 77.5010),
    "ew_central_3": (12.9236, 77.5012),
    "ew_central_4": (12.9236, 77.5014),
    "ew_central_5": (12.9236, 77.5016),
    
    # East-West Road 3 (Central Middle)
    "ew_mid_1": (12.9232, 77.5008),
    "ew_mid_2": (12.9232, 77.5010),
    "ew_mid_3": (12.9232, 77.5012),
    "ew_mid_4": (12.9232, 77.5014),
    "ew_mid_5": (12.9232, 77.5016),
    
    # East-West Road 4 (Southern)
    "ew_south_1": (12.9228, 77.5008),
    "ew_south_2": (12.9228, 77.5010),
    "ew_south_3": (12.9228, 77.5012),
    "ew_south_4": (12.9228, 77.5014),
    "ew_south_5": (12.9228, 77.5016),
    
    # North-South Road 2 (Middle)
    "ns_mid_1": (12.9241, 77.5012),
    "ns_mid_2": (12.9238, 77.5012),
    "ns_mid_3": (12.9235, 77.5012),
    "ns_mid_4": (12.9232, 77.5012),
    "ns_mid_5": (12.9229, 77.5012),
    
    # North-South Road 3 (Eastern)
    "ns_east_1": (12.9241, 77.5015),
    "ns_east_2": (12.9238, 77.5015),
    "ns_east_3": (12.9235, 77.5015),
    "ns_east_4": (12.9232, 77.5015),
    "ns_east_5": (12.9229, 77.5015),
    
    # Campus Exits
    "main_gate": (12.9241, 77.5008),
    "pattanagere_metro_exit": (12.9241, 77.4985),
    "south_exit": (12.9222, 77.5016),
    "east_exit": (12.9231, 77.5018),
}


CAMPUS_EDGES = [
    # Main North-South Road (RV Road)
    ("rv_road_north", "rv_road_1", 25),
    ("rv_road_1", "rv_road_2", 25),
    ("rv_road_2", "rv_road_3", 25),
    ("rv_road_3", "rv_road_4", 25),
    ("rv_road_4", "rv_road_5", 25),
    ("rv_road_5", "rv_road_6", 25),
    ("rv_road_6", "rv_road_7", 25),
    ("rv_road_7", "rv_road_south", 25),
    
    # East-West Road 1 (Northern) connections
    ("ew_north_1", "ew_north_2", 25),
    ("ew_north_2", "ew_north_3", 25),
    ("ew_north_3", "ew_north_4", 25),
    
    # East-West Road 2 (Central Upper) connections
    ("ew_central_1", "ew_central_2", 25),
    ("ew_central_2", "ew_central_3", 25),
    ("ew_central_3", "ew_central_4", 25),
    ("ew_central_4", "ew_central_5", 25),
    
    # East-West Road 3 (Central Middle) connections
    ("ew_mid_1", "ew_mid_2", 25),
    ("ew_mid_2", "ew_mid_3", 25),
    ("ew_mid_3", "ew_mid_4", 25),
    ("ew_mid_4", "ew_mid_5", 25),
    
    # East-West Road 4 (Southern) connections
    ("ew_south_1", "ew_south_2", 25),
    ("ew_south_2", "ew_south_3", 25),
    ("ew_south_3", "ew_south_4", 25),
    ("ew_south_4", "ew_south_5", 25),
    
    # North-South Road 2 (Middle) connections
    ("ns_mid_1", "ns_mid_2", 25),
    ("ns_mid_2", "ns_mid_3", 25),
    ("ns_mid_3", "ns_mid_4", 25),
    ("ns_mid_4", "ns_mid_5", 25),
    
    # North-South Road 3 (Eastern) connections
    ("ns_east_1", "ns_east_2", 25),
    ("ns_east_2", "ns_east_3", 25),
    ("ns_east_3", "ns_east_4", 25),
    ("ns_east_4", "ns_east_5", 25),
    
    # Intersections - RV Road with East-West roads
    ("rv_road_north", "ew_north_1", 15),
    ("rv_road_3", "ew_central_1", 15),
    ("rv_road_5", "ew_mid_1", 15),
    ("rv_road_7", "ew_south_1", 15),
    
    # Intersections - Middle NS Road with East-West roads  
    ("ns_mid_1", "ew_north_2", 15),
    ("ew_central_3", "ns_mid_3", 15),
    ("ew_mid_3", "ns_mid_4", 15),
    ("ew_south_3", "ns_mid_5", 15),
    
    # Intersections - Eastern NS Road with East-West roads
    ("ns_east_1", "ew_north_3", 15),
    ("ew_central_4", "ns_east_3", 15),
    ("ew_mid_4", "ns_east_4", 15),
    ("ew_south_4", "ns_east_5", 15),
    
    # Campus Exit Connections
    ("main_gate", "rv_road_north", 20),
    ("main_gate", "ew_north_1", 25),
    
    ("pattanagere_metro_exit", "rv_road_north", 200),
    
    ("south_exit", "rv_road_south", 60),
    ("south_exit", "ew_south_5", 45),
    
    ("east_exit", "ew_mid_5", 30),
    ("east_exit", "ns_east_4", 40),
]


CAMPUS_EXITS = {
    "main_gate": (12.9241, 77.5008),
    "pattanagere_metro_exit": (12.9241, 77.4985),
    "south_exit": (12.9222, 77.5016),
    "east_exit": (12.9231, 77.5018),
}


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
