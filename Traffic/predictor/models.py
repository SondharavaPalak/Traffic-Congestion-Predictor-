from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count
import json


class UserProfile(models.Model):
    """Extended user profile with traffic-specific preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='traffic_profile')
    preferred_mode = models.CharField(
        max_length=50,
        choices=[('Car', 'Car'), ('Metro', 'Metro'), ('Bike', 'Bike'), ('Walk', 'Walk')],
        default='Car'
    )
    car_make = models.CharField(max_length=100, blank=True, null=True)
    car_mileage_kmpl = models.FloatField(default=12.0, help_text="Kilometers per liter")
    fuel_cost_per_liter = models.FloatField(default=100.0)
    bike_mileage_kmpl = models.FloatField(default=50.0)
    primary_city = models.CharField(max_length=100, blank=True)
    favorite_destinations = models.JSONField(default=list, blank=True)
    commute_time_preference = models.CharField(
        max_length=50,
        choices=[('Fast', 'Fastest'), ('Balanced', 'Balanced Cost-Time'), ('Cheap', 'Cheapest')],
        default='Balanced'
    )
    enable_notifications = models.BooleanField(default=True)
    notification_threshold = models.CharField(
        max_length=50,
        choices=[('Low', 'Low Traffic'), ('Medium', 'Medium Traffic'), ('High', 'High Traffic')],
        default='High'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Prediction(models.Model):
    CONGESTION_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    MODE_CHOICES = [
        ('Car', 'Car'),
        ('Metro', 'Metro'),
        ('Bike', 'Bike'),
        ('Walk', 'Walk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='predictions')
    created_at = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    source_lat = models.FloatField()
    source_lon = models.FloatField()
    dest_lat = models.FloatField()
    dest_lon = models.FloatField()
    distance_km = models.FloatField()
    hour = models.IntegerField()
    weekday = models.IntegerField()
    day_type = models.CharField(max_length=50)
    weather = models.CharField(max_length=100)
    event_flag = models.BooleanField(default=False)
    route_type = models.CharField(max_length=50)
    congestion_level = models.CharField(max_length=10, choices=CONGESTION_CHOICES)
    suggested_mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    probabilities = models.JSONField(default=dict, blank=True)  # {Low, Medium, High probabilities}
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.city}: {self.source} → {self.destination} ({self.congestion_level})"


class TripHistory(models.Model):
    """Completed trips with actual observed congestion"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_histories')
    prediction = models.OneToOneField(Prediction, on_delete=models.SET_NULL, null=True, blank=True, related_name='trip_history')
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance_km = models.FloatField()
    predicted_congestion = models.CharField(max_length=50, help_text="What was predicted")
    actual_congestion = models.CharField(
        max_length=50,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        help_text="What actually happened"
    )
    predicted_duration_mins = models.IntegerField(null=True, blank=True)
    actual_duration_mins = models.IntegerField(null=True, blank=True)
    mode_used = models.CharField(max_length=50, choices=Prediction.MODE_CHOICES)
    fuel_cost = models.FloatField(default=0)
    toll_cost = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    travel_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-travel_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.city} ({self.travel_date.date()})"


class PredictionAccuracy(models.Model):
    """Tracks prediction accuracy metrics over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='accuracy_records')
    city = models.CharField(max_length=100)
    date = models.DateField()
    total_predictions = models.IntegerField(default=0)
    correct_predictions = models.IntegerField(default=0)
    accuracy_percentage = models.FloatField(default=0.0)
    avg_confidence = models.FloatField(default=0.0)
    low_accuracy = models.IntegerField(default=0)
    medium_accuracy = models.IntegerField(default=0)
    high_accuracy = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']
    
    def __str__(self):
        return f"{self.city} - {self.date}: {self.accuracy_percentage}%"


class RouteOption(models.Model):
    """Alternative routes for route optimization"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='route_options')
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    waypoints = models.JSONField(default=list, blank=True)  # List of intermediate stops
    route_rank = models.IntegerField(default=1)  # 1=best, 2=alternate1, 3=alternate2
    distance_km = models.FloatField()
    expected_duration_mins = models.IntegerField()
    expected_congestion = models.CharField(max_length=50)
    estimated_cost = models.FloatField(default=0)
    mode = models.CharField(max_length=50, choices=Prediction.MODE_CHOICES)
    route_details = models.JSONField(default=dict)  # Store detailed route info
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['route_rank']
    
    def __str__(self):
        return f"Route {self.route_rank} - {self.city}"


class TripCost(models.Model):
    """Cost analysis for trips"""
    trip_history = models.OneToOneField(TripHistory, on_delete=models.CASCADE, related_name='cost_details')
    distance_km = models.FloatField()
    mode = models.CharField(max_length=50)
    fuel_cost = models.FloatField(default=0)
    toll_cost = models.FloatField(default=0)
    parking_cost = models.FloatField(default=0)
    metro_cost = models.FloatField(default=0)
    bike_rental_cost = models.FloatField(default=0)
    total_cost = models.FloatField()
    cost_per_km = models.FloatField()
    time_saved_mins = models.IntegerField(default=0, help_text="Time saved vs slow route")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cost: ₹{self.total_cost} - {self.mode}"


class PeakHourPattern(models.Model):
    """Historical peak hour patterns"""
    city = models.CharField(max_length=100)
    weekday = models.IntegerField(choices=[(i, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]) for i in range(7)])
    hour = models.IntegerField()
    route_type = models.CharField(max_length=50)
    avg_congestion_score = models.FloatField(help_text="0-1 scale")
    congestion_probability_low = models.FloatField()
    congestion_probability_medium = models.FloatField()
    congestion_probability_high = models.FloatField()
    frequency = models.IntegerField(help_text="How many times observed")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['city', 'weekday', 'hour']
        unique_together = ['city', 'weekday', 'hour', 'route_type']
    
    def __str__(self):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return f"{self.city} - {days[self.weekday]} {self.hour}:00"


class AnalyticsSnapshot(models.Model):
    """Daily/hourly analytics snapshots"""
    city = models.CharField(max_length=100)
    date = models.DateField()
    hour = models.IntegerField(null=True, blank=True)  # NULL for daily snapshots
    total_predictions = models.IntegerField(default=0)
    avg_congestion_score = models.FloatField(default=0.0)
    avg_prediction_accuracy = models.FloatField(default=0.0)
    low_congestion_count = models.IntegerField(default=0)
    medium_congestion_count = models.IntegerField(default=0)
    high_congestion_count = models.IntegerField(default=0)
    avg_trip_duration_mins = models.FloatField(default=0.0)
    avg_trip_cost = models.FloatField(default=0.0)
    peak_hour = models.IntegerField(null=True, blank=True)
    busiest_route = models.CharField(max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-hour']
        unique_together = ['city', 'date', 'hour']
    
    def __str__(self):
        return f"{self.city} - {self.date}" + (f" Hour {self.hour}" if self.hour else " (Daily)")


class SavedScenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_scenarios')
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    is_favorite = models.BooleanField(default=False)
    visit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_count', '-updated_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}"
