from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random
import requests
from datetime import datetime, timedelta

from .models import Prediction
from .services.model import predictor


def home(request):
    """Home page with hero section and feature cards"""
    return render(request, 'predictor/home.html')


def predict_view(request):
    """Main prediction page"""
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata']
    
    if request.method == 'POST':
        city = request.POST.get('city')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        
        if city and source and destination:
            # Make prediction
            result = predictor.predict_traffic(city, source, destination)
            
            # Save prediction to database
            prediction = Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                city=city,
                source=source,
                destination=destination,
                source_lat=result['coordinates']['source'][0],
                source_lon=result['coordinates']['source'][1],
                dest_lat=result['coordinates']['destination'][0],
                dest_lon=result['coordinates']['destination'][1],
                distance_km=result['features']['distance_km'],
                hour=result['features']['hour'],
                weekday=result['features']['weekday'],
                day_type=result['features']['day_type'],
                weather=result['features']['weather'],
                event_flag=result['features']['event'],
                route_type=result['features']['route_type'],
                congestion_level=result['congestion_level'],
                suggested_mode=result['suggested_mode']
            )
            
            context = {
                'cities': cities,
                'prediction': prediction,
                'result': result,
                'show_result': True
            }
        else:
            messages.error(request, 'Please fill in all fields.')
            context = {'cities': cities}
    else:
        context = {'cities': cities}
    
    return render(request, 'predictor/predict.html', context)


@csrf_exempt
def predict_ajax(request):
    """AJAX endpoint for predictions"""
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get('city')
        source = data.get('source')
        destination = data.get('destination')
        
        if city and source and destination:
            result = predictor.predict_traffic(city, source, destination)
            return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def news_view(request):
    """Traffic news page"""
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata']
    selected_city = request.GET.get('city', 'Delhi')
    
    # Try to fetch news from NewsAPI
    news_articles = []
    try:
        # You can add your NewsAPI key here
        api_key = "your_newsapi_key"  # Replace with actual key
        query = f"traffic {selected_city}"
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            news_articles = data.get('articles', [])[:10]
        else:
            raise Exception("API request failed")
    except Exception as e:
        print(f"News API error: {e}")
        # Fallback: generate synthetic news
        news_articles = generate_synthetic_news(selected_city)
    
    context = {
        'cities': cities,
        'selected_city': selected_city,
        'news_articles': news_articles
    }
    return render(request, 'predictor/news.html', context)


def generate_synthetic_news(city):
    """Generate synthetic traffic news when API is unavailable"""
    headlines_and_content = [
        {
            'title': f"Traffic congestion expected on major roads in {city} during peak hours",
            'content': f"Commuters in {city} are advised to plan their journeys carefully as traffic congestion is expected on major arterial roads during peak hours today. The traffic police have identified several bottlenecks including main intersections and highway entry points. Alternative routes are recommended for faster travel."
        },
        {
            'title': f"New metro line to reduce traffic in {city} by 30%",
            'content': f"The newly inaugurated metro line in {city} is expected to significantly reduce road traffic by up to 30% according to transport authorities. The line connects major commercial and residential areas, providing commuters with a faster and more reliable alternative to road transport."
        },
        {
            'title': f"Smart traffic signals installed across {city} to improve flow",
            'content': f"The {city} municipal corporation has installed AI-powered smart traffic signals at 50 major intersections. These signals adapt to real-time traffic conditions and are expected to reduce waiting times by 25% and improve overall traffic flow throughout the city."
        },
        {
            'title': f"Construction work on {city} highways may cause delays",
            'content': f"Ongoing construction work on major highways in {city} may cause significant delays for commuters over the next two weeks. The public works department advises using alternative routes and allowing extra travel time. Work is being conducted during off-peak hours where possible."
        },
        {
            'title': f"Traffic police launch new initiative to reduce congestion in {city}",
            'content': f"The {city} traffic police have launched a comprehensive initiative to tackle traffic congestion. The program includes deployment of additional personnel at key intersections, improved signal timing, and a public awareness campaign about traffic rules and safe driving practices."
        },
        {
            'title': f"Public transport usage increases in {city} as fuel prices rise",
            'content': f"With rising fuel prices, more commuters in {city} are switching to public transport. Bus ridership has increased by 15% over the past month, while metro usage has grown by 20%. Transport authorities are considering increasing service frequency to meet growing demand."
        },
        {
            'title': f"New flyover project to ease traffic in {city} city center",
            'content': f"A new flyover project in {city} city center is set to begin next month. The project aims to reduce traffic congestion at one of the busiest intersections in the city. The flyover is expected to be completed within 18 months and will significantly improve traffic flow."
        },
        {
            'title': f"Traffic advisory issued for {city} due to upcoming festival",
            'content': f"The {city} traffic police have issued an advisory for the upcoming festival celebrations. Several roads will be closed or have restricted access. Commuters are advised to use public transport and avoid the city center during festival hours. Additional parking arrangements have been made."
        },
        {
            'title': f"Bike lanes to be expanded across {city} to promote cycling",
            'content': f"The {city} municipal corporation has announced plans to expand dedicated bike lanes across the city. The initiative aims to promote cycling as an eco-friendly mode of transport and reduce vehicular traffic. The project will cover 100 kilometers of roads over the next year."
        },
        {
            'title': f"Traffic monitoring system upgraded in {city} with AI technology",
            'content': f"The traffic monitoring system in {city} has been upgraded with artificial intelligence technology. The new system can predict traffic patterns, detect accidents in real-time, and automatically adjust signal timings. This is expected to reduce travel time by up to 20%."
        }
    ]
    
    sources = ['Times of India', 'Hindustan Times', 'The Hindu', 'Economic Times', 'Indian Express']
    
    news_articles = []
    for i, article_data in enumerate(headlines_and_content):
        news_articles.append({
            'title': article_data['title'],
            'content': article_data['content'],
            'source': {'name': random.choice(sources)},
            'url': f"/news/article/{i+1}/",
            'publishedAt': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
        })
    
    return news_articles


def news_article_detail(request, article_id):
    """Display individual news article"""
    # Get the synthetic news articles
    news_articles = generate_synthetic_news("Delhi")  # Default city for article lookup
    
    try:
        article_index = int(article_id) - 1
        if 0 <= article_index < len(news_articles):
            article = news_articles[article_index]
            context = {
                'article': article,
                'article_id': article_id
            }
            return render(request, 'predictor/news_detail.html', context)
        else:
            raise ValueError("Article not found")
    except (ValueError, IndexError):
        messages.error(request, 'Article not found.')
        return redirect('news')


def dashboard_view(request):
    """Dashboard with traffic statistics and charts"""
    # Get all recent predictions
    recent_predictions = Prediction.objects.all()[:10]
    
    # Calculate congestion statistics based on all predictions
    all_predictions = Prediction.objects.all()
    total_predictions = all_predictions.count()
    low_congestion = all_predictions.filter(congestion_level='Low').count()
    medium_congestion = all_predictions.filter(congestion_level='Medium').count()
    high_congestion = all_predictions.filter(congestion_level='High').count()
    
    # Generate chart data
    chart_data = generate_chart_data()
    
    context = {
        'recent_predictions': recent_predictions,
        'chart_data': chart_data,
        'total_predictions': total_predictions,
        'low_congestion': low_congestion,
        'medium_congestion': medium_congestion,
        'high_congestion': high_congestion,
    }
    return render(request, 'predictor/dashboard.html', context)


def generate_chart_data():
    """Generate synthetic chart data for dashboard"""
    # Peak hour trend data
    hours = list(range(24))
    congestion_levels = []
    for hour in hours:
        if 8 <= hour <= 10 or 17 <= hour <= 19:
            congestion_levels.append(random.randint(70, 90))
        elif 7 <= hour <= 11 or 16 <= hour <= 20:
            congestion_levels.append(random.randint(50, 70))
        else:
            congestion_levels.append(random.randint(20, 50))
    
    # Route type congestion data
    route_types = ['Local', 'Suburban', 'Highway']
    route_congestion = [random.randint(60, 80), random.randint(40, 60), random.randint(30, 50)]
    
    return {
        'peak_hours': {
            'labels': hours,
            'data': congestion_levels
        },
        'route_types': {
            'labels': route_types,
            'data': route_congestion
        }
    }


def about_view(request):
    """About page with ML workflow explanation"""
    return render(request, 'predictor/about.html')


# ============================================================================
# NEW ANALYTICS & USER PROFILE VIEWS
# ============================================================================

@csrf_exempt
def analytics_dashboard(request):
    """Main analytics dashboard"""
    from .services.analytics import analytics_service
    from .models import UserProfile, TripHistory
    
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata']
    selected_city = request.GET.get('city', 'Delhi')
    
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access analytics.')
        return redirect('home')
    
    try:
        # Get user profile
        user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
        
        # Get analytics data
        accuracy_data = analytics_service.calculate_prediction_accuracy(selected_city, days=30)
        peak_hours = analytics_service.get_peak_hour_analysis(selected_city)
        trends = analytics_service.get_historical_trends(selected_city, days=90)
        cost_analysis = analytics_service.get_cost_analysis(request.user, selected_city, days=30)
        busiest_hours = analytics_service.get_busiest_hours(selected_city, limit=5)
        
        # User trip statistics
        user_trips = TripHistory.objects.filter(user=request.user, city=selected_city).count()
        avg_cost = TripHistory.objects.filter(
            user=request.user, city=selected_city
        ).aggregate(Avg('total_cost'))['total_cost__avg'] or 0
        
        context = {
            'cities': cities,
            'selected_city': selected_city,
            'user_profile': user_profile,
            'accuracy_data': accuracy_data,
            'peak_hours': peak_hours[:5],  # Top 5 peak hours
            'trends_summary': trends.get('summary', {}),
            'cost_analysis': cost_analysis,
            'busiest_hours': busiest_hours,
            'user_trips': user_trips,
            'avg_cost': round(avg_cost, 2),
        }
    except Exception as e:
        logger.error(f"Error loading analytics: {e}")
        context = {'cities': cities, 'selected_city': selected_city, 'error': str(e)}
    
    return render(request, 'predictor/analytics_dashboard.html', context)


@csrf_exempt
def user_profile_view(request):
    """User profile and preferences management"""
    from .models import UserProfile
    
    if not request.user.is_authenticated:
        return redirect('home')
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_profile.preferred_mode = request.POST.get('preferred_mode', user_profile.preferred_mode)
        user_profile.car_make = request.POST.get('car_make', user_profile.car_make)
        user_profile.car_mileage_kmpl = float(request.POST.get('car_mileage_kmpl', user_profile.car_mileage_kmpl))
        user_profile.fuel_cost_per_liter = float(request.POST.get('fuel_cost_per_liter', user_profile.fuel_cost_per_liter))
        user_profile.primary_city = request.POST.get('primary_city', user_profile.primary_city)
        user_profile.commute_time_preference = request.POST.get('commute_time_preference', user_profile.commute_time_preference)
        user_profile.enable_notifications = bool(request.POST.get('enable_notifications'))
        user_profile.notification_threshold = request.POST.get('notification_threshold', user_profile.notification_threshold)
        user_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    context = {
        'user_profile': user_profile,
        'modes': ['Car', 'Metro', 'Bike', 'Walk'],
        'preferences': ['Fast', 'Balanced', 'Cheap'],
        'thresholds': ['Low', 'Medium', 'High'],
    }
    return render(request, 'predictor/user_profile.html', context)


@csrf_exempt
def trip_history_view(request):
    """View trip history with filtering and analysis"""
    from .models import TripHistory
    
    if not request.user.is_authenticated:
        return redirect('home')
    
    # Get filter parameters
    city_filter = request.GET.get('city')
    mode_filter = request.GET.get('mode')
    sort_by = request.GET.get('sort', '-travel_date')
    
    # Build query
    trips = TripHistory.objects.filter(user=request.user)
    
    if city_filter:
        trips = trips.filter(city=city_filter)
    if mode_filter:
        trips = trips.filter(mode_used=mode_filter)
    
    # Apply sorting
    if sort_by in ['-travel_date', 'travel_date', 'total_cost', '-total_cost']:
        trips = trips.order_by(sort_by)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(trips, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_trips = TripHistory.objects.filter(user=request.user).count()
    total_distance = TripHistory.objects.filter(user=request.user).aggregate(
        Sum('distance_km'))['distance_km__sum'] or 0
    total_cost = TripHistory.objects.filter(user=request.user).aggregate(
        Sum('total_cost'))['total_cost__sum'] or 0
    
    context = {
        'page_obj': page_obj,
        'total_trips': total_trips,
        'total_distance': round(total_distance, 2),
        'total_cost': round(total_cost, 2),
        'cities': ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata'],
        'modes': ['Car', 'Metro', 'Bike', 'Walk'],
        'current_filters': {
            'city': city_filter,
            'mode': mode_filter,
        }
    }
    return render(request, 'predictor/trip_history.html', context)


@csrf_exempt
def route_optimization_view(request):
    """Route optimization and comparison"""
    from .services.route_optimization import route_optimizer
    from .services.costs import cost_calculator
    
    if request.method == 'POST':
        data = json.loads(request.body)
        source_coords = (data.get('source_lat'), data.get('source_lon'))
        dest_coords = (data.get('dest_lat'), data.get('dest_lon'))
        distance_km = data.get('distance_km', 0)
        route_type = data.get('route_type', 'local')
        duration_mins = data.get('duration_mins', 30)
        
        try:
            # Generate alternative routes
            routes = route_optimizer.generate_alternative_routes(source_coords, dest_coords, num_alternatives=3)
            
            # Calculate costs for each route
            costs_per_route = {}
            for route in routes:
                route_id = route['route_id']
                route_distance = route['distance_km']
                cost_breakdown = cost_calculator.calculate_car_cost(route_distance, route_type, duration_mins)
                costs_per_route[str(route_id)] = cost_breakdown['total_cost']
                route['cost_breakdown'] = cost_breakdown
            
            # Optimize routes
            optimized_routes = route_optimizer.optimize_for_cost(distance_km, routes, costs_per_route)
            
            return JsonResponse({
                'success': True,
                'routes': optimized_routes,
            })
        except Exception as e:
            logger.error(f"Route optimization error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    context = {}
    return render(request, 'predictor/route_optimization.html', context)


@csrf_exempt
def saved_destinations_view(request):
    """Manage favorite/saved destinations"""
    from .models import SavedScenario
    
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            scenario, created = SavedScenario.objects.get_or_create(
                user=request.user,
                name=request.POST.get('name'),
                city=request.POST.get('city'),
                source=request.POST.get('source'),
                destination=request.POST.get('destination'),
                defaults={'is_favorite': True}
            )
            messages.success(request, f"Destination '{scenario.name}' saved successfully!")
        
        elif action == 'toggle_favorite':
            scenario_id = request.POST.get('scenario_id')
            scenario = SavedScenario.objects.get(id=scenario_id, user=request.user)
            scenario.is_favorite = not scenario.is_favorite
            scenario.save()
            messages.success(request, "Favorite status updated!")
        
        elif action == 'delete':
            scenario_id = request.POST.get('scenario_id')
            SavedScenario.objects.filter(id=scenario_id, user=request.user).delete()
            messages.success(request, "Destination deleted!")
        
        return redirect('saved_destinations')
    
    # Get saved scenarios
    saved_scenarios = SavedScenario.objects.filter(user=request.user).order_by('-is_favorite', '-visit_count')
    favorites = saved_scenarios.filter(is_favorite=True)
    
    context = {
        'saved_scenarios': saved_scenarios,
        'favorites': favorites,
        'cities': ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata'],
    }
    return render(request, 'predictor/saved_destinations.html', context)


@csrf_exempt
def predict_with_options_ajax(request):
    """Enhanced prediction with route options and cost comparison"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        city = data.get('city')
        source = data.get('source')
        destination = data.get('destination')
        
        # Get base prediction
        result = predictor.predict_traffic(city, source, destination)
        
        # Generate route options
        from .services.route_optimization import route_optimizer
        from .services.costs import cost_calculator
        
        source_coords = (result['coordinates']['source'][0], result['coordinates']['source'][1])
        dest_coords = (result['coordinates']['destination'][0], result['coordinates']['destination'][1])
        distance = result['features']['distance_km']
        route_type = result['features']['route_type']
        
        routes = route_optimizer.generate_alternative_routes(source_coords, dest_coords, 3)
        cost_comparison = cost_calculator.compare_modes_cost(distance, route_type=route_type)
        
        # Save prediction if user is authenticated
        if request.user.is_authenticated:
            prediction = Prediction.objects.create(
                user=request.user,
                city=city,
                source=source,
                destination=destination,
                source_lat=result['coordinates']['source'][0],
                source_lon=result['coordinates']['source'][1],
                dest_lat=result['coordinates']['destination'][0],
                dest_lon=result['coordinates']['destination'][1],
                distance_km=result['features']['distance_km'],
                hour=result['features']['hour'],
                weekday=result['features']['weekday'],
                day_type=result['features']['day_type'],
                weather=result['features']['weather'],
                event_flag=result['features']['event'],
                route_type=result['features']['route_type'],
                congestion_level=result['congestion_level'],
                suggested_mode=result['suggested_mode'],
                probabilities=result.get('probabilities', {})
            )
        
        return JsonResponse({
            'success': True,
            'prediction': result,
            'routes': routes,
            'cost_comparison': cost_comparison,
        })
    except Exception as e:
        logger.error(f"Error in predict with options: {e}")
        return JsonResponse({'error': str(e)}, status=400)


# Add necessary imports at the top
import logging
from django.db.models import Sum, Avg, Count
logger = logging.getLogger(__name__)





