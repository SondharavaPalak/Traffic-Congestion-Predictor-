from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('predict/', views.predict_view, name='predict'),
    path('news/', views.news_view, name='news'),
    path('news/article/<int:article_id>/', views.news_article_detail, name='news_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    
    # AJAX endpoints
    path('predict-ajax/', views.predict_ajax, name='predict_ajax'),
    
    # NEW: Analytics & User Features
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('trip-history/', views.trip_history_view, name='trip_history'),
    path('route-optimization/', views.route_optimization_view, name='route_optimization'),
    path('saved-destinations/', views.saved_destinations_view, name='saved_destinations'),
    
    # NEW: Enhanced AJAX endpoint
    path('predict-with-options/', views.predict_with_options_ajax, name='predict_with_options'),
] 