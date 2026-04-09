import pandas as pd
import numpy as np
import random
import datetime
from math import radians, sin, cos, sqrt, atan2
import holidays

# Define cities and bounding boxes for coordinates (rough ranges)
cities = {
    "Delhi": (28.4, 28.9, 76.8, 77.4),
    "Mumbai": (18.8, 19.3, 72.7, 73.1),
    "Bengaluru": (12.8, 13.1, 77.4, 77.8),
    "Hyderabad": (17.2, 17.6, 78.3, 78.6),
    "Chennai": (12.9, 13.2, 80.1, 80.3),
    "Kolkata": (22.4, 22.7, 88.2, 88.5),
}

# Indian holidays
indian_holidays = holidays.India(years=[2024, 2025])

def random_coord(city_box):
    lat = round(random.uniform(city_box[0], city_box[1]), 6)
    lon = round(random.uniform(city_box[2], city_box[3]), 6)
    return lat, lon

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return round(R*2*atan2(sqrt(a), sqrt(1-a)), 2)

def get_weather(month):
    if month in [6,7,8,9]:  # Monsoon
        return random.choice(["Rainy", "Humid", "Cloudy"])
    elif month in [12,1,2]: # Winter
        return random.choice(["Cold", "Foggy", "Clear"])
    else:
        return random.choice(["Sunny", "Clear", "Hot"])

def generate_data(n=5000):
    rows = []
    start_date = datetime.date(2024,1,1)
    for _ in range(n):
        city = random.choice(list(cities.keys()))
        slat, slon = random_coord(cities[city])
        dlat, dlon = random_coord(cities[city])
        distance = haversine(slat, slon, dlat, dlon)
        
        # Time features
        date = start_date + datetime.timedelta(days=random.randint(0, 365))
        hour = random.randint(0,23)
        weekday = date.strftime("%A")
        day_type = "Holiday" if date in indian_holidays else "Weekend" if weekday in ["Saturday","Sunday"] else "Weekday"

        weather = get_weather(date.month)
        event = 1 if random.random() < 0.2 and hour in [18,19,20] else 0
        route_type = random.choice(["Highway","Arterial","Local"])

        # Congestion score logic
        score = 0
        if hour in range(8,11) or hour in range(17,20): score += 2
        if day_type == "Holiday": score += 2
        if day_type == "Weekend": score += 1
        if weather in ["Rainy","Foggy"]: score += 1
        if distance > 15: score += 1
        if event: score += 2

        if score <= 2: congestion = "Low"
        elif score <= 4: congestion = "Medium"
        else: congestion = "High"

        if congestion == "Low": mode = "Car"
        elif congestion == "Medium": mode = "Metro"
        else: mode = "Bike/Walk"

        rows.append([city,slat,slon,dlat,dlon,distance,date,weekday,hour,day_type,weather,event,route_type,congestion,mode])
    
    return pd.DataFrame(rows,columns=[
        "city","source_lat","source_lon","dest_lat","dest_lon","distance_km","date","weekday","hour","day_type","weather","event","route_type","congestion_level","suggested_mode"
    ])

df = generate_data(5000)
df.to_csv("traffic_dataset.csv",index=False)
print(df.head())
