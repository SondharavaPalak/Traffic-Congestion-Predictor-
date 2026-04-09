"""
Analytics service for generating insights and historical trends
Handles trend analysis, accuracy calculation, peak hour patterns, and reports
"""

import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta, date
from django.db.models import Avg, Count, Q, F
import json

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Generates analytics and insights from traffic data"""
    
    def __init__(self):
        """Initialize analytics service"""
        pass
    
    def calculate_prediction_accuracy(self, city: str, days: int = 30) -> Dict:
        """
        Calculate prediction accuracy for a city
        
        Args:
            city: City name
            days: Number of days to analyze
        
        Returns:
            Accuracy metrics and breakdown
        """
        try:
            from predictor.models import TripHistory
            from django.utils import timezone
            
            cutoff_date = timezone.now() - timedelta(days=days)
            trips = TripHistory.objects.filter(
                city=city,
                travel_date__gte=cutoff_date
            )
            
            if not trips.exists():
                return {
                    'total_predictions': 0,
                    'accurate_predictions': 0,
                    'overall_accuracy': 0,
                    'by_congestion_level': {},
                }
            
            total = trips.count()
            correct = trips.filter(
                predicted_congestion=F('actual_congestion')
            ).count()
            
            accuracy = round((correct / total * 100), 2) if total > 0 else 0
            
            # Breakdown by congestion level
            breakdown = {}
            for level in ['Low', 'Medium', 'High']:
                level_trips = trips.filter(predicted_congestion=level)
                if level_trips.exists():
                    level_total = level_trips.count()
                    level_correct = level_trips.filter(
                        actual_congestion=level
                    ).count()
                    breakdown[level] = {
                        'predictions': level_total,
                        'correct': level_correct,
                        'accuracy': round((level_correct / level_total * 100), 2) if level_total > 0 else 0,
                    }
            
            return {
                'city': city,
                'period_days': days,
                'total_predictions': total,
                'accurate_predictions': correct,
                'overall_accuracy': accuracy,
                'by_congestion_level': breakdown,
                'calculated_at': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error calculating accuracy: {e}")
            return {}
    
    def get_peak_hour_analysis(self, city: str, weekday: Optional[int] = None) -> List[Dict]:
        """
        Analyze peak hours for a city
        
        Args:
            city: City name
            weekday: 0-6 (Mon-Sun), None for all days
        
        Returns:
            Peak hour patterns sorted by congestion
        """
        try:
            from predictor.models import PeakHourPattern
            
            query = PeakHourPattern.objects.filter(city=city).order_by('-avg_congestion_score')
            if weekday is not None:
                query = query.filter(weekday=weekday)
            
            results = []
            for pattern in query[:24]:  # Maximum 24 hours
                results.append({
                    'hour': pattern.hour,
                    'weekday': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][pattern.weekday],
                    'route_type': pattern.route_type,
                    'congestion_score': round(pattern.avg_congestion_score, 2),
                    'congestion_probabilities': {
                        'low': round(pattern.congestion_probability_low, 2),
                        'medium': round(pattern.congestion_probability_medium, 2),
                        'high': round(pattern.congestion_probability_high, 2),
                    },
                    'frequency': pattern.frequency,
                })
            
            return results
        except Exception as e:
            logger.error(f"Error getting peak hour analysis: {e}")
            return []
    
    def get_busiest_hours(self, city: str, limit: int = 5) -> List[Dict]:
        """Get top busiest hours for a city"""
        try:
            from predictor.models import PeakHourPattern
            
            patterns = PeakHourPattern.objects.filter(city=city).order_by('-avg_congestion_score')[:limit]
            
            results = []
            for pattern in patterns:
                day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][pattern.weekday]
                results.append({
                    'rank': len(results) + 1,
                    'day': day_name,
                    'hour': f"{pattern.hour}:00",
                    'congestion_score': round(pattern.avg_congestion_score, 2),
                    'route_type': pattern.route_type,
                    'probability_high': round(pattern.congestion_probability_high * 100, 1),
                })
            
            return results
        except Exception as e:
            logger.error(f"Error getting busiest hours: {e}")
            return []
    
    def get_historical_trends(self, city: str, days: int = 90) -> Dict:
        """
        Get historical trends over time
        
        Args:
            city: City name
            days: Number of days to analyze
        
        Returns:
            Trend data (congestion average, prediction volume, etc.)
        """
        try:
            from predictor.models import AnalyticsSnapshot
            from django.utils import timezone
            
            cutoff_date = timezone.now().date() - timedelta(days=days)
            snapshots = AnalyticsSnapshot.objects.filter(
                city=city,
                date__gte=cutoff_date,
                hour__isnull=True  # Daily snapshots only
            ).order_by('date')
            
            if not snapshots.exists():
                return {'trends': [], 'summary': {}}
            
            trends = []
            for snapshot in snapshots:
                trends.append({
                    'date': snapshot.date.isoformat(),
                    'predictions': snapshot.total_predictions,
                    'avg_congestion_score': round(snapshot.avg_congestion_score, 2),
                    'accuracy': round(snapshot.avg_prediction_accuracy, 2),
                    'peak_hour': snapshot.peak_hour,
                    'avg_trip_duration': round(snapshot.avg_trip_duration_mins, 1),
                    'avg_trip_cost': round(snapshot.avg_trip_cost, 2),
                })
            
            # Calculate summary statistics
            avg_congestion = sum(t['avg_congestion_score'] for t in trends) / len(trends) if trends else 0
            avg_accuracy = sum(t['accuracy'] for t in trends) / len(trends) if trends else 0
            
            summary = {
                'period_days': days,
                'avg_congestion_score': round(avg_congestion, 2),
                'avg_prediction_accuracy': round(avg_accuracy, 2),
                'total_predictions': sum(t['predictions'] for t in trends),
                'worst_day': trends[-1] if trends else None,  # Highest congestion
                'best_day': trends[0] if trends else None,    # Lowest congestion
            }
            
            return {
                'city': city,
                'trends': trends,
                'summary': summary,
            }
        except Exception as e:
            logger.error(f"Error getting historical trends: {e}")
            return {'trends': [], 'summary': {}}
    
    def get_cost_analysis(self, user, city: str, days: int = 30) -> Dict:
        """
        Analyze spending patterns for a user
        
        Args:
            user: User object
            city: City name
            days: Number of days to analyze
        
        Returns:
            Cost breakdown and insights
        """
        try:
            from predictor.models import TripHistory
            from django.utils import timezone
            
            cutoff_date = timezone.now() - timedelta(days=days)
            trips = TripHistory.objects.filter(
                user=user,
                city=city,
                travel_date__gte=cutoff_date
            )
            
            if not trips.exists():
                return {
                    'total_trips': 0,
                    'total_cost': 0,
                    'cost_breakdown': {},
                }
            
            total_trips = trips.count()
            total_fuel_cost = trips.aggregate(Avg('fuel_cost'))['fuel_cost__sum'] or 0
            total_toll_cost = trips.aggregate(Avg('toll_cost'))['toll_cost__sum'] or 0
            total_parking_cost = trips.aggregate(Avg('parking_cost'))['parking_cost__sum'] or 0
            total_cost = sum([total_fuel_cost, total_toll_cost, total_parking_cost])
            
            # Cost by mode
            by_mode = {}
            for trip in trips:
                mode = trip.mode_used
                if mode not in by_mode:
                    by_mode[mode] = {'trips': 0, 'cost': 0, 'distance': 0}
                by_mode[mode]['trips'] += 1
                by_mode[mode]['cost'] += trip.total_cost
                by_mode[mode]['distance'] += trip.distance_km
            
            for mode in by_mode:
                by_mode[mode]['avg_cost_per_trip'] = round(
                    by_mode[mode]['cost'] / by_mode[mode]['trips'], 2
                ) if by_mode[mode]['trips'] > 0 else 0
                by_mode[mode]['avg_distance'] = round(
                    by_mode[mode]['distance'] / by_mode[mode]['trips'], 2
                ) if by_mode[mode]['trips'] > 0 else 0
            
            return {
                'city': city,
                'period_days': days,
                'total_trips': total_trips,
                'total_cost': round(total_cost, 2),
                'avg_cost_per_trip': round(total_cost / total_trips, 2) if total_trips > 0 else 0,
                'cost_breakdown': {
                    'fuel': round(total_fuel_cost, 2),
                    'toll': round(total_toll_cost, 2),
                    'parking': round(total_parking_cost, 2),
                },
                'by_mode': by_mode,
            }
        except Exception as e:
            logger.error(f"Error calculating cost analysis: {e}")
            return {}
    
    def get_route_statistics(self, city: str, limit: int = 10) -> List[Dict]:
        """
        Get most frequently traveled routes
        
        Args:
            city: City name
            limit: Number of routes to return
        
        Returns:
            Top routes with statistics
        """
        try:
            from predictor.models import Prediction
            
            routes = Prediction.objects.filter(city=city).values(
                'source', 'destination'
            ).annotate(
                count=Count('id'),
                avg_congestion=Avg('congestion_level'),
            ).order_by('-count')[:limit]
            
            results = []
            for idx, route in enumerate(routes, 1):
                results.append({
                    'rank': idx,
                    'source': route['source'],
                    'destination': route['destination'],
                    'predictions': route['count'],
                    'avg_congestion': str(route['avg_congestion']),
                })
            
            return results
        except Exception as e:
            logger.error(f"Error getting route statistics: {e}")
            return []
    
    def get_weather_impact_analysis(self, city: str, days: int = 30) -> Dict:
        """
        Analyze impact of weather on congestion
        
        Args:
            city: City name
            days: Number of days to analyze
        
        Returns:
            Weather vs congestion correlation
        """
        try:
            from predictor.models import Prediction
            from django.utils import timezone
            
            cutoff_date = timezone.now() - timedelta(days=days)
            predictions = Prediction.objects.filter(
                city=city,
                created_at__gte=cutoff_date
            )
            
            weather_impact = {}
            for prediction in predictions:
                weather = prediction.weather
                congestion = prediction.congestion_level
                
                if weather not in weather_impact:
                    weather_impact[weather] = {'Low': 0, 'Medium': 0, 'High': 0, 'total': 0}
                
                weather_impact[weather][congestion] += 1
                weather_impact[weather]['total'] += 1
            
            # Convert to percentages
            for weather in weather_impact:
                total = weather_impact[weather]['total']
                if total > 0:
                    weather_impact[weather] = {
                        'Low': round(weather_impact[weather]['Low'] / total * 100, 1),
                        'Medium': round(weather_impact[weather]['Medium'] / total * 100, 1),
                        'High': round(weather_impact[weather]['High'] / total * 100, 1),
                        'total_predictions': total,
                    }
            
            return {
                'city': city,
                'period_days': days,
                'weather_impact': weather_impact,
            }
        except Exception as e:
            logger.error(f"Error analyzing weather impact: {e}")
            return {}
    
    def generate_monthly_report(self, city: str, month: int, year: int) -> Dict:
        """
        Generate comprehensive monthly report
        
        Args:
            city: City name
            month: Month number (1-12)
            year: Year
        
        Returns:
            Monthly report with all metrics
        """
        try:
            from predictor.models import TripHistory, AnalyticsSnapshot
            from django.utils import timezone
            
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            
            snapshots = AnalyticsSnapshot.objects.filter(
                city=city,
                date__gte=start_date,
                date__lte=end_date,
                hour__isnull=True
            )
            
            if not snapshots.exists():
                return {}
            
            total_predictions = snapshots.aggregate(Count('id'))['id__count']
            avg_congestion = snapshots.aggregate(Avg('avg_congestion_score'))['avg_congestion_score__avg'] or 0
            avg_accuracy = snapshots.aggregate(Avg('avg_prediction_accuracy'))['avg_prediction_accuracy__avg'] or 0
            
            return {
                'city': city,
                'period': f"{month}/{year}",
                'total_predictions': total_predictions,
                'avg_congestion_score': round(avg_congestion, 2),
                'avg_prediction_accuracy': round(avg_accuracy, 2),
                'total_days_analyzed': snapshots.count(),
            }
        except Exception as e:
            logger.error(f"Error generating monthly report: {e}")
            return {}


# Global analytics service instance
analytics_service = AnalyticsService()
