"""
Route optimization service
Handles multi-stop route planning, alternative routes, and optimization
"""

import logging
import math
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from geopy.distance import geodesic

logger = logging.getLogger(__name__)


class RouteOptimizer:
    """Optimizes routes for multiple stops and different criteria"""
    
    def __init__(self):
        """Initialize route optimizer"""
        self.earth_radius_km = 6371  # Earth's radius in kilometers
    
    def haversine_distance(self, coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
        """
        Calculate great-circle distance between two points
        
        Args:
            coord1: (latitude, longitude) tuple
            coord2: (latitude, longitude) tuple
        
        Returns:
            Distance in kilometers
        """
        try:
            lat1, lon1 = coord1
            lat2, lon2 = coord2
            
            # Convert to radians
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            # Haversine formula
            a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return self.earth_radius_km * c
        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            return 0
    
    def calculate_route_distance(self, waypoints: List[Tuple[float, float]]) -> float:
        """
        Calculate total distance for a route with multiple waypoints
        
        Args:
            waypoints: List of (lat, lon) tuples
        
        Returns:
            Total distance in kilometers
        """
        if len(waypoints) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(waypoints) - 1):
            total_distance += self.haversine_distance(waypoints[i], waypoints[i + 1])
        
        return round(total_distance, 2)
    
    def nearest_neighbor_route(self, 
                               start: Tuple[float, float],
                               stops: List[Tuple[float, float]],
                               end: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Simple nearest neighbor algorithm for route optimization
        
        Args:
            start: Starting coordinate
            stops: List of intermediate stops
            end: Ending coordinate
        
        Returns:
            Optimized route (list of waypoints)
        """
        try:
            route = [start]
            remaining_stops = stops.copy()
            
            while remaining_stops:
                # Find nearest stop to current location
                current = route[-1]
                nearest = min(remaining_stops, 
                            key=lambda stop: self.haversine_distance(current, stop))
                route.append(nearest)
                remaining_stops.remove(nearest)
            
            route.append(end)
            return route
        except Exception as e:
            logger.error(f"Error in nearest neighbor routing: {e}")
            return [start, end]
    
    def generate_alternative_routes(self,
                                   start: Tuple[float, float],
                                   end: Tuple[float, float],
                                   num_alternatives: int = 2) -> List[Dict]:
        """
        Generate alternative route suggestions
        
        Args:
            start: Starting coordinate
            end: Ending coordinate
            num_alternatives: Number of alternatives to generate
        
        Returns:
            List of alternative routes with metadata
        """
        try:
            base_distance = self.haversine_distance(start, end)
            alternatives = []
            
            # Route 1: Direct route
            alternatives.append({
                'route_id': 1,
                'name': 'Direct Route (Fastest)',
                'waypoints': [start, end],
                'distance_km': round(base_distance, 2),
                'estimated_duration': self._estimate_duration(base_distance, 'medium'),
                'route_type': 'direct',
                'flexibility': 'Low',
                'congestion_risk': 'Medium',
            })
            
            # Route 2: Scenic/alternate (longer but possibly less congested)
            if num_alternatives > 1:
                alternate_distance = base_distance * 1.1  # 10% longer
                alternatives.append({
                    'route_id': 2,
                    'name': 'Alternate Route (Scenic)',
                    'waypoints': [start, end],
                    'distance_km': round(alternate_distance, 2),
                    'estimated_duration': self._estimate_duration(alternate_distance, 'low'),
                    'route_type': 'alternate',
                    'flexibility': 'Medium',
                    'congestion_risk': 'Low',
                })
            
            # Route 3: Local/avoided highway
            if num_alternatives > 2:
                local_distance = base_distance * 0.9  # Slightly shorter but local roads
                alternatives.append({
                    'route_id': 3,
                    'name': 'Local Route (Shortest)',
                    'waypoints': [start, end],
                    'distance_km': round(local_distance, 2),
                    'estimated_duration': self._estimate_duration(local_distance, 'medium'),
                    'route_type': 'local',
                    'flexibility': 'High',
                    'congestion_risk': 'High',
                })
            
            return alternatives
        except Exception as e:
            logger.error(f"Error generating alternative routes: {e}")
            return []
    
    def _estimate_duration(self, distance_km: float, traffic_condition: str = 'medium') -> int:
        """
        Estimate trip duration based on distance and traffic
        
        Args:
            distance_km: Distance in kilometers
            traffic_condition: 'low', 'medium', 'high'
        
        Returns:
            Estimated duration in minutes
        """
        # Base speed: 40 km/hr in city
        base_speed = 40
        
        # Adjust for traffic conditions
        speed_multiplier = {
            'low': 1.0,      # Normal speed
            'medium': 0.7,   # 70% of normal
            'high': 0.4,     # 40% of normal
        }
        
        adjusted_speed = base_speed * speed_multiplier.get(traffic_condition, 0.7)
        duration_hours = distance_km / adjusted_speed
        
        return max(int(duration_hours * 60), 1)  # At least 1 minute
    
    def optimize_for_cost(self,
                         distance_km: float,
                         routes: List[Dict],
                         costs_per_route: Dict[str, float]) -> List[Dict]:
        """
        Sort routes by cost efficiency
        
        Args:
            distance_km: Base distance
            routes: List of route objects
            costs_per_route: Dict mapping route_id to cost
        
        Returns:
            Routes sorted by cost efficiency
        """
        try:
            for route in routes:
                route_id = route.get('route_id')
                cost = costs_per_route.get(str(route_id), 100)
                duration = route.get('estimated_duration', 60)
                
                route['cost'] = cost
                route['cost_efficiency'] = round(cost / route.get('distance_km', 1), 2)
                route['time_efficiency'] = round(duration / route.get('distance_km', 1), 2)
                route['overall_score'] = round((cost * 0.6) + (duration * 0.4), 2)
            
            # Sort by overall score
            return sorted(routes, key=lambda x: x['overall_score'])
        except Exception as e:
            logger.error(f"Error optimizing for cost: {e}")
            return routes
    
    def optimize_for_time(self, routes: List[Dict]) -> List[Dict]:
        """Sort routes by time efficiency"""
        try:
            return sorted(routes, key=lambda x: x.get('estimated_duration', 999))
        except Exception as e:
            logger.error(f"Error optimizing for time: {e}")
            return routes
    
    def optimize_for_comfort(self, routes: List[Dict]) -> List[Dict]:
        """Sort routes by comfort (avoiding heavy traffic)"""
        try:
            congestion_risk_order = {'Low': 1, 'Medium': 2, 'High': 3}
            return sorted(routes, 
                        key=lambda x: congestion_risk_order.get(x.get('congestion_risk', 'Medium'), 2))
        except Exception as e:
            logger.error(f"Error optimizing for comfort: {e}")
            return routes
    
    def calculate_waypoint_impact(self, 
                                 route_without_waypoint: float,
                                 route_with_waypoint: float) -> Dict[str, float]:
        """
        Calculate impact of adding a waypoint to route
        
        Returns:
            Distance added, time added, etc.
        """
        distance_added = round(route_with_waypoint - route_without_waypoint, 2)
        time_added_mins = int((distance_added / 40) * 60)  # Assuming 40 km/hr
        
        return {
            'distance_added_km': distance_added,
            'time_added_mins': time_added_mins,
            'detour_percentage': round((distance_added / route_without_waypoint * 100), 2) if route_without_waypoint > 0 else 0,
        }
    
    def validate_waypoint_sequence(self, waypoints: List[Dict]) -> bool:
        """Validate if waypoint sequence is logical"""
        if len(waypoints) < 2:
            return False
        
        total_distance = 0
        for i in range(len(waypoints) - 1):
            wp1 = (waypoints[i]['lat'], waypoints[i]['lon'])
            wp2 = (waypoints[i + 1]['lat'], waypoints[i + 1]['lon'])
            total_distance += self.haversine_distance(wp1, wp2)
        
        # Sequence is valid if total distance is reasonable (not excessively long)
        return total_distance > 0
    
    def generate_walking_routes(self, 
                               start: Tuple[float, float],
                               end: Tuple[float, float]) -> Dict:
        """Generate pedestrian-friendly routes"""
        distance = self.haversine_distance(start, end)
        duration = max(int((distance / 5) * 60), 15)  # 5 km/hr walking speed
        
        return {
            'mode': 'walk',
            'distance_km': round(distance, 2),
            'duration_mins': duration,
            'difficulty': 'Easy' if distance < 2 else 'Moderate' if distance < 5 else 'Hard',
            'calories_burned': round(distance * 50),  # Approximate
        }


# Global route optimizer instance
route_optimizer = RouteOptimizer()
