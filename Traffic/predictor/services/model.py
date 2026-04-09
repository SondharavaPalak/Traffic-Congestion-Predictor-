import pickle
import os
import random
import logging
from typing import Tuple, Dict, List, Any
from datetime import datetime
import holidays
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

logger = logging.getLogger(__name__)


class TrafficPredictor:

    CITY_COORDS = {
        'Delhi': (28.7041, 77.1025),
        'Mumbai': (19.0760, 72.8777),
        'Bengaluru': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
    }

    WEATHER_CONDITIONS = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
    WEATHER_WEIGHTS = [0.5, 0.3, 0.15, 0.05]

    ROUTE_TYPE_THRESHOLDS = {
        'local': 5,
        'suburban': 20
    }

    PEAK_HOURS = [
        (8, 10),
        (17, 19)
    ]

    def __init__(self):
        self.model = None
        self.geolocator = Nominatim(user_agent="traffic_predictor")
        self.india_holidays = holidays.India()
        self.supported_cities = list(self.CITY_COORDS.keys())

        self.load_model()

    def load_model(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), "traffic_model.pkl")
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)
                logger.info("Model loaded successfully")
            else:
                logger.warning("Model file not found, using fallback")
        except Exception as e:
            logger.error(f"Error loading model: {e}")

    def get_coordinates(self, location: str) -> Tuple[float, float]:
        try:
            loc = self.geolocator.geocode(f"{location}, India", timeout=10)
            if loc:
                return (loc.latitude, loc.longitude)
        except Exception as e:
            logger.warning(f"Geocoding failed: {e}")

        for city, coords in self.CITY_COORDS.items():
            if city.lower() in location.lower():
                return coords

        return (random.uniform(8, 37), random.uniform(68, 97))

    def calculate_distance(self, lat1, lon1, lat2, lon2) -> float:
        distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
        return round(max(0.1, min(distance, 200)), 2)

    def get_weather_data(self, city):
        try:
            api_key = os.getenv('OPENWEATHER_API_KEY')
            if api_key:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}"
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    return res.json()['weather'][0]['main']
        except:
            pass

        return random.choices(self.WEATHER_CONDITIONS, weights=self.WEATHER_WEIGHTS)[0]

    def get_route_type(self, distance):
        if distance < self.ROUTE_TYPE_THRESHOLDS['local']:
            return 'local'
        elif distance < self.ROUTE_TYPE_THRESHOLDS['suburban']:
            return 'suburban'
        return 'highway'

    def get_day_type(self, now):
        if now.date() in self.india_holidays:
            return 'Holiday'
        elif now.weekday() in [5, 6]:
            return 'Weekend'
        return 'Weekday'

    def get_event_flag(self, hour, weekday):
        return (
            (weekday in [5, 6] and 10 <= hour <= 22) or
            (weekday in range(5) and 18 <= hour <= 21)
        )

    def predict(self, features: Dict[str, Any]) -> Tuple[str, List[float]]:
        try:
            if self.model:
                model = self.model['model']
                pred = model.predict([list(features.values())])[0]
                probs = model.predict_proba([list(features.values())])[0].tolist()
                label = self.model['target_le'].classes_[pred]
                return label, probs
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")

        return self._fallback_prediction(features)

    def _fallback_prediction(self, features):
        score = 0

        distance = features['distance_km']
        hour = features['hour']
        weekday = features['weekday']
        weather = features['weather']
        event = features['event']

        if distance > 20:
            score += 2
        elif distance > 10:
            score += 1

        if any(start <= hour <= end for start, end in self.PEAK_HOURS):
            score += 2
        elif 7 <= hour <= 20:
            score += 1

        if weekday in [5, 6]:
            score += 1

        if weather in ['Rain', 'Thunderstorm']:
            score += 1

        if event:
            score += 1

        if score >= 4:
            return 'High', [0.1, 0.2, 0.7]
        elif score >= 2:
            return 'Medium', [0.2, 0.6, 0.2]
        return 'Low', [0.7, 0.2, 0.1]

    def suggest_mode(self, congestion_level, distance):
        if distance <= 2:
            return 'Walk'
        elif distance <= 8:
            return 'Metro' if congestion_level == 'High' else 'Bike'
        return 'Metro' if congestion_level == 'High' else 'Car'

    def validate_city(self, city):
        if city not in self.supported_cities:
            raise ValueError(f"Unsupported city: {city}")

    def predict_traffic(self, city, source, destination):
        self.validate_city(city)

        source_lat, source_lon = self.get_coordinates(source)
        dest_lat, dest_lon = self.get_coordinates(destination)

        distance = self.calculate_distance(source_lat, source_lon, dest_lat, dest_lon)

        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()

        day_type = self.get_day_type(now)
        weather = self.get_weather_data(city)
        event_flag = self.get_event_flag(hour, weekday)
        route_type = self.get_route_type(distance)

        features = {
            'city': city,
            'distance_km': distance,
            'hour': hour,
            'weekday': weekday,
            'day_type': day_type,
            'weather': weather,
            'event': event_flag,
            'route_type': route_type
        }

        congestion, probs = self.predict(features)
        mode = self.suggest_mode(congestion, distance)

        return {
            'congestion_level': congestion,
            'suggested_mode': mode,
            'probabilities': probs,
            'features': features,
            'coordinates': {
                'source': (source_lat, source_lon),
                'destination': (dest_lat, dest_lon)
            }
        }


# Global instance
predictor = TrafficPredictor()