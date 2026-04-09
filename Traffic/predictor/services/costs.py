"""
Cost calculation service for different transport modes
Handles fuel costs, tolls, parking, and other expenses
"""

import logging
from typing import Dict, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class CostCalculator:
    """Calculates trip costs for different transportation modes"""
    
    # Default Indian cost parameters (can be configured per user)
    DEFAULT_FUEL_COST_PER_LITER = 100.0  # ₹ per liter
    DEFAULT_MILEAGE_CAR = 12.0  # km/liter
    DEFAULT_MILEAGE_BIKE = 50.0  # km/liter
    DEFAULT_PARKING_COST_PER_HOUR = 30.0  # ₹
    DEFAULT_METRO_COST_BASE = 10.0  # ₹
    DEFAULT_BIKE_RENTAL_PER_KM = 2.0  # ₹/km
    
    # Toll rates for different routes (highway vs local)
    TOLL_RATES = {
        'highway': 1.5,  # ₹ per km
        'suburban': 0.8,  # ₹ per km
        'local': 0.0,  # ₹ per km (no tolls)
    }
    
    # Metro fare formula: Base + (Distance / 5) * rate
    METRO_FARE_STRUCTURE = {
        'base': 10,  # ₹
        'per_km_rate': 5,  # ₹ per 5km
    }
    
    def __init__(self, user_profile=None):
        """Initialize with optional user preferences"""
        self.user_profile = user_profile
        self.fuel_cost_per_liter = self.DEFAULT_FUEL_COST_PER_LITER
        self.mileage_car = self.DEFAULT_MILEAGE_CAR
        self.mileage_bike = self.DEFAULT_MILEAGE_BIKE
        
        if user_profile:
            self.fuel_cost_per_liter = user_profile.fuel_cost_per_liter or self.DEFAULT_FUEL_COST_PER_LITER
            self.mileage_car = user_profile.car_mileage_kmpl or self.DEFAULT_MILEAGE_CAR
            self.mileage_bike = user_profile.bike_mileage_kmpl or self.DEFAULT_MILEAGE_BIKE
    
    def calculate_car_cost(self, distance_km: float, route_type: str = 'local', 
                          duration_mins: int = 0) -> Dict[str, float]:
        """
        Calculate car travel cost
        
        Args:
            distance_km: Distance in kilometers
            route_type: 'local', 'suburban', or 'highway'
            duration_mins: Trip duration in minutes (for parking)
        
        Returns:
            Dict with fuel_cost, toll_cost, parking_cost, total_cost
        """
        try:
            # Fuel cost
            liters_needed = distance_km / self.mileage_car
            fuel_cost = liters_needed * self.fuel_cost_per_liter
            
            # Toll cost
            toll_rate = self.TOLL_RATES.get(route_type, 0)
            toll_cost = distance_km * toll_rate
            
            # Parking cost (assuming 1 hour parking at destination)
            parking_cost = self.DEFAULT_PARKING_COST_PER_HOUR
            
            total_cost = fuel_cost + toll_cost + parking_cost
            
            return {
                'fuel_cost': round(fuel_cost, 2),
                'toll_cost': round(toll_cost, 2),
                'parking_cost': round(parking_cost, 2),
                'total_cost': round(total_cost, 2),
                'cost_per_km': round(total_cost / distance_km, 2) if distance_km > 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error calculating car cost: {e}")
            return {
                'fuel_cost': 0,
                'toll_cost': 0,
                'parking_cost': 0,
                'total_cost': 0,
                'cost_per_km': 0,
            }
    
    def calculate_bike_cost(self, distance_km: float, route_type: str = 'local') -> Dict[str, float]:
        """Calculate bike travel cost"""
        try:
            liters_needed = distance_km / self.mileage_bike
            fuel_cost = liters_needed * self.fuel_cost_per_liter
            
            # Minimal toll for bikes
            toll_cost = distance_km * 0.3
            
            # No parking cost for bikes
            parking_cost = 0
            
            total_cost = fuel_cost + toll_cost
            
            return {
                'fuel_cost': round(fuel_cost, 2),
                'toll_cost': round(toll_cost, 2),
                'parking_cost': 0,
                'total_cost': round(total_cost, 2),
                'cost_per_km': round(total_cost / distance_km, 2) if distance_km > 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error calculating bike cost: {e}")
            return {'fuel_cost': 0, 'toll_cost': 0, 'parking_cost': 0, 'total_cost': 0, 'cost_per_km': 0}
    
    def calculate_metro_cost(self, distance_km: float) -> Dict[str, float]:
        """Calculate metro/transit cost"""
        try:
            # Simple fare structure: base + (distance / 5) km blocks
            km_blocks = (distance_km + 4) // 5  # Round up to nearest 5km
            fare = self.METRO_FARE_STRUCTURE['base'] + (km_blocks * self.METRO_FARE_STRUCTURE['per_km_rate'])
            
            # Ensure maximum metro fare is not exceeded
            fare = min(fare, 100)
            
            return {
                'metro_cost': round(fare, 2),
                'total_cost': round(fare, 2),
                'cost_per_km': round(fare / distance_km, 2) if distance_km > 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error calculating metro cost: {e}")
            return {'metro_cost': 0, 'total_cost': 0, 'cost_per_km': 0}
    
    def calculate_walk_cost(self, distance_km: float) -> Dict[str, float]:
        """Calculate walk cost (typically free)"""
        return {
            'total_cost': 0,
            'cost_per_km': 0,
        }
    
    def calculate_bike_rental_cost(self, distance_km: float, duration_mins: int = 30) -> Dict[str, float]:
        """Calculate bike rental cost"""
        try:
            # Standard bike rental: ₹2/km or ₹1/min, whichever is higher
            distance_cost = distance_km * self.DEFAULT_BIKE_RENTAL_PER_KM
            time_cost = max(duration_mins // 30, 1) * 50  # ₹50 per 30 mins
            
            total_cost = max(distance_cost, time_cost)
            
            return {
                'rental_cost': round(total_cost, 2),
                'total_cost': round(total_cost, 2),
                'cost_per_km': round(total_cost / distance_km, 2) if distance_km > 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error calculating bike rental cost: {e}")
            return {'rental_cost': 0, 'total_cost': 0, 'cost_per_km': 0}
    
    def compare_modes_cost(self, distance_km: float, duration_mins: int = 30, 
                          route_type: str = 'local') -> Dict[str, Dict]:
        """
        Compare costs across all transport modes
        
        Returns:
            Dict with cost breakdown for each mode, ranked by total cost
        """
        try:
            costs = {
                'car': self.calculate_car_cost(distance_km, route_type, duration_mins),
                'bike': self.calculate_bike_cost(distance_km, route_type),
                'metro': self.calculate_metro_cost(distance_km),
                'walk': self.calculate_walk_cost(distance_km),
                'bike_rental': self.calculate_bike_rental_cost(distance_km, duration_mins),
            }
            
            # Add mode names and rank by total cost
            for mode, cost_data in costs.items():
                cost_data['mode'] = mode
                cost_data['total_cost'] = cost_data.get('total_cost', 0)
            
            # Sort by total cost
            ranked = sorted(costs.items(), key=lambda x: x[1]['total_cost'])
            
            result = {}
            for idx, (mode, cost_data) in enumerate(ranked, 1):
                cost_data['rank'] = idx
                result[mode] = cost_data
            
            return result
        except Exception as e:
            logger.error(f"Error comparing mode costs: {e}")
            return {}
    
    def calculate_time_value(self, time_saved_mins: int, user_hourly_rate: float = 500) -> float:
        """
        Calculate monetary value of time saved
        
        Args:
            time_saved_mins: Minutes saved
            user_hourly_rate: Assumed hourly rate (₹)
        
        Returns:
            Money equivalent of time saved
        """
        hours_saved = time_saved_mins / 60
        return hours_saved * user_hourly_rate
    
    def calculate_breakeven_analysis(self, car_cost: float, metro_cost: float, 
                                    time_difference_mins: int = 10) -> Dict[str, float]:
        """
        Analyze cost-benefit of different modes
        
        Returns breakeven points and savings
        """
        cost_difference = car_cost - metro_cost
        time_value = self.calculate_time_value(abs(time_difference_mins))
        
        return {
            'cost_difference': round(cost_difference, 2),
            'time_value_saved': round(time_value, 2),
            'net_saving': round(cost_difference + time_value, 2),
            'breakeven_trips_per_month': round(abs(cost_difference) / 30, 1) if cost_difference != 0 else 0,
        }


# Global cost calculator instance
cost_calculator = CostCalculator()
