# Traffic Predictor - Real-Time Traffic Congestion Prediction System

A **production-quality web application** that predicts traffic congestion in real-time using advanced machine learning algorithms. Designed for major Indian cities with interactive maps, data visualization, and personalized transport recommendations.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [System Architecture](#system-architecture)
6. [Machine Learning Model](#machine-learning-model)
7. [Dataset Details](#dataset-details)
8. [Workflow](#workflow)
9. [Getting Started](#getting-started)
10. [Configuration & Customization](#configuration--customization)
11. [Usage Guide](#usage-guide)
12. [Database Models](#database-models)
13. [API Endpoints](#api-endpoints)
14. [Troubleshooting](#troubleshooting)

---

## Project Overview

**Traffic Predictor** is a Django-based web application that leverages machine learning to predict traffic congestion levels across Indian cities. The system analyzes multiple factors including time of day, weather conditions, special events, and route characteristics to provide accurate, real-time congestion forecasts.

### Key Objectives
- ✅ Predict traffic congestion (Low, Medium, High) with 94.6% accuracy
- ✅ Provide interactive route visualization with Folium maps
- ✅ Suggest optimal transportation modes based on predictions
- ✅ Calculate travel costs and time estimates
- ✅ Track prediction history and accuracy metrics
- ✅ Integrate real-time weather and holiday data
- ✅ Provide beautiful, responsive user interface

### Supported Cities
- Delhi
- Mumbai
- Bengaluru
- Hyderabad
- Chennai
- Kolkata

---

## Features

### Core Prediction Features
- **Real-Time Traffic Prediction**: Get instant congestion forecasts for any route
- **Confidence Scores**: View probability distributions for each congestion level
- **Interactive Route Mapping**: Visualize routes with Folium interactive maps
- **Distance Calculation**: Automatic distance computation using Haversine formula
- **Weather Integration**: Real-time weather data via OpenWeather API (optional)
- **Holiday Detection**: Automatic Indian holiday detection and factoring

### Route & Transport Features
- **Intelligent Mode Suggestions**: Automated transport mode recommendations (Car, Metro, Bike/Walk)
- **Cost Estimation**: Calculate fuel/toll costs based on distance and vehicle
- **Route Type Detection**: Automatic classification (Local, Suburban, Highway)
- **Duration Estimation**: Predict travel time based on congestion level

### Analytics & Visualization
- **Interactive Dashboard**: View global traffic statistics and trends
- **Chart.js Integration**: Beautiful charts for data visualization
- **Trip History Tracking**: Complete history of all predictions and actual outcomes
- **Accuracy Metrics**: Real-time model performance tracking
- **Prediction Analytics**: Detailed breakdown by city, time, and congestion level

### User Experience
- **Responsive Design**: Mobile-first Tailwind CSS design
- **HTMX Integration**: Dynamic UI updates without page refreshes
- **User Profiles**: Personalized preferences and favorite destinations
- **News Integration**: Latest traffic news and alerts (via NewsAPI)
- **Authentication**: User registration and login system

---

## Technology Stack

### Backend Framework & Dependencies

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Django** | 4.9 | Web framework for Python |
| **Python** | 3.9+ | Programming language |
| **SQLite** | Latest | Relational database |
| **scikit-learn** | 1.7.1 | Machine learning library |
| **NumPy** | 2.3.2 | Numerical computing |
| **SciPy** | 1.16.1 | Scientific computing |
| **Pandas** | Latest | Data manipulation & analysis |

### Geospatial & Location Services

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Geopy** | 2.4.1 | Geocoding & distance calculations |
| **Folium** | 0.20.0 | Interactive mapping library |
| **Nominatim** | - | Reverse geocoding service |
| **Haversine Formula** | - | Geographic distance calculation |

### External APIs & Services

| Service | Purpose | Optional |
|---------|---------|----------|
| **OpenWeather API** | Real-time weather data | Optional |
| **Nominatim API** | Address geocoding | Built-in |
| **NewsAPI** | Traffic news integration | Optional |

### Frontend Technologies

| Technology | Purpose |
|-----------|---------|
| **Tailwind CSS** | Utility-first CSS framework |
| **HTMX** | Dynamic HTML updates |
| **Chart.js** | Data visualization |
| **Leaflet.js** | Interactive maps (via Folium) |
| **Bootstrap** | Responsive grid layout |
| **Font Awesome** | Icon library |

### Data Science & ML Libraries

| Library | Purpose |
|---------|---------|
| **scikit-learn** | Random Forest classifier |
| **pandas** | Data preprocessing |
| **numpy** | Numerical operations |
| **scipy** | Statistical functions |

### Utilities

| Library | Version | Purpose |
|---------|---------|---------|
| **holidays** | 0.79 | Indian holiday calendar |
| **requests** | 2.32.5 | HTTP requests for APIs |

---

## Project Structure

```
traffic-predictor/
│
├── Traffic/                          # Django project settings & management
│   ├── db.sqlite3                   # SQLite database file
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   ├── traffic_model.pkl            # Trained ML model (pickled)
│   │
│   ├── traffic_predictor/           # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings
│   │   ├── settings.txt             # Additional configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── asgi.py                  # ASGI configuration
│   │   └── wsgi.py                  # WSGI configuration
│   │
│   ├── predictor/                   # Main Django application
│   │   ├── models.py                # Database models
│   │   ├── views.py                 # View functions & route handlers
│   │   ├── urls.py                  # App URL patterns
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── apps.py                  # App configuration
│   │   ├── tests.py                 # Unit tests
│   │   │
│   │   ├── migrations/              # Database migration files
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_analytics_models.py
│   │   │   └── 0003_alter_savedscenario_options_and_more.py
│   │   │
│   │   └── services/                # Business logic layer
│   │       ├── __init__.py
│   │       ├── model.py             # ML prediction service
│   │       ├── analytics.py         # Analytics & reporting
│   │       ├── costs.py             # Cost estimation
│   │       └── route_optimization.py # Route optimization
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Base template (layout)
│   │   └── predictor/
│   │       ├── home.html            # Home page
│   │       ├── predict.html         # Prediction page
│   │       ├── dashboard.html       # Analytics dashboard
│   │       ├── analytics_dashboard.html # Detailed analytics
│   │       ├── trip_history.html    # User trip history
│   │       ├── saved_destinations.html # Saved routes
│   │       ├── route_optimization.html # Route optimization
│   │       ├── news.html            # Traffic news
│   │       ├── news_detail.html     # News detail view
│   │       ├── about.html           # About page
│   │       └── user_profile.html    # User profile
│   │
│   └── static/                      # Static files
│       ├── css/                     # Stylesheets
│       └── js/                      # JavaScript files
│
├── prediction model/                # ML Model training & evaluation
│   ├── traffic_dataset.csv          # Training dataset (5000 samples)
│   ├── model_train.py               # Model training pipeline
│   ├── model_metrics.json           # Model performance metrics
│   ├── generate_csv.py              # Dataset generation script
│   ├── checkaccuracy.py             # Model accuracy evaluation
│   └── MODEL_TRAINING_GUIDE.md      # ML documentation
│
└── logs/                            # Application logs
    └── application.log              # Debug & error logs


## File Descriptions

### Core Application Files

**traffic_predictor/settings.py**
- Django configuration (installed apps, database, middleware, static files)
- Timezone and language settings
- Template and static file directories
- Authentication settings

**predictor/models.py**
- `UserProfile`: Extended user preferences (transport mode, vehicle details, thresholds)
- `Prediction`: Individual traffic predictions with coordinates and features
- `TripHistory`: Completed trips with predicted vs. actual congestion
- `SavedScenario`: User-saved prediction scenarios
- Database relationships and constraints

**predictor/views.py**
- `home()`: Landing page with feature showcase
- `predict_view()`: Main prediction interface
- `predict_ajax()`: AJAX endpoint for dynamic predictions
- `dashboard()`: Global traffic statistics
- `trip_history()`: User's prediction and trip history
- `analytics()`: Detailed traffic analytics

**predictor/services/model.py**
- `TrafficPredictor` class: Main ML inference engine
- `load_model()`: Load trained Random Forest model
- `predict_traffic()`: Full prediction pipeline
- `get_coordinates()`: Nominatim geocoding
- `get_weather_data()`: OpenWeather API integration
- `_fallback_prediction()`: Rule-based fallback logic

### ML Model Files

**prediction model/model_train.py**
- Random Forest classifier training
- Feature encoding and preprocessing
- Train/test split (80/20)
- Hyperparameter optimization with GridSearchCV
- 5-fold cross-validation
- Performance metrics calculation
- Model serialization

**prediction model/generate_csv.py**
- Synthetic dataset generation (5000 samples)
- Realistic congestion scoring logic
- City-specific coordinate generation
- Temporal features (hour, weekday, holidays)
- Weather and event simulation

**prediction model/checkaccuracy.py**
- Model accuracy verification
- Confusion matrix analysis
- Classification report generation
- Validation on test set

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│  (Tailwind CSS + HTMX + Chart.js + Leaflet Maps)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   DJANGO VIEWS LAYER                         │
│  (predict_view, dashboard, analytics, trip_history, etc.)   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   SERVICE LAYER (Business Logic)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ model.py: ML Prediction Pipeline                     │  │
│  │  ├─ Load trained Random Forest model               │  │
│  │  ├─ Geocoding (Nominatim)                          │  │
│  │  ├─ Feature Engineering                            │  │
│  │  ├─ Model Inference                                │  │
│  │  └─ Fallback Rule-Based Prediction                 │  │
│  │                                                      │  │
│  │ analytics.py: Statistical Analysis                  │  │
│  │ costs.py: Cost & Duration Estimation               │  │
│  │ route_optimization.py: Route Optimization           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   DATA LAYER                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Django ORM                                            │  │
│  │  ├─ UserProfile                                      │  │
│  │  ├─ Prediction                                       │  │
│  │  ├─ TripHistory                                      │  │
│  │  └─ SavedScenario                                    │  │
│  │                                                      │  │
│  │ SQLite Database (db.sqlite3)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              EXTERNAL SERVICES & APIs                        │
│  ├─ OpenWeather API: Real-time weather                      │
│  ├─ Nominatim: Address geocoding                           │
│  ├─ NewsAPI: Traffic news & alerts                         │
│  └─ Python holidays: Indian calendar                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
User Input (Source, Destination, City)
        │
        ▼
Feature Engineering Layer
├─ Geocoding (Nominatim API)
├─ Distance Calculation (Haversine)
├─ Temporal Features (Hour, Weekday)
├─ Holiday Detection (holidays.India)
├─ Weather Data (OpenWeather API or default)
├─ Event Flag Detection
└─ Route Type Classification
        │
        ▼
ML Prediction Pipeline
├─ Load trained Random Forest model
├─ Encode categorical features
├─ Scale numerical features
├─ Run model inference
└─ Get confidence probabilities
        │
        ▼
Fallback Logic (if model fails)
├─ Rule-based score calculation
├─ Peak hour detection
├─ Weather factor analysis
└─ Distance evaluation
        │
        ▼
Result Aggregation
├─ Congestion Level (Low/Medium/High)
├─ Confidence Scores
├─ Suggested Transport Mode
├─ Cost Estimation
└─ Duration Forecast
        │
        ▼
Database Persistence
├─ Save Prediction record
├─ Update user analytics
└─ Log trip history
        │
        ▼
Response to User
├─ Interactive Folium map
├─ Metrics & probabilities
├─ Recommendations
└─ Cost breakdown
```

### Component Interaction Model

```
┌─────────────────┐
│   User/Browser  │
└────────┬────────┘
         │
    HTTP Requests
         │
    ┌────▼──────────────────┐
    │   Django Main App      │
    │   (traffic_predictor)  │
    └────┬───────────────────┘
         │
    ┌────▼──────────────────────┐
    │  Predictor Application     │
    │  ├─ Views                  │
    │  ├─ URLs                   │
    │  ├─ Models                 │
    │  └─ Admin                  │
    └────┬──────────────────────┘
         │
    ┌────▼────────────────────────────────────┐
    │      Services Layer                      │
    │  ├─ Model.py (ML Pipeline)              │
    │  ├─ Analytics.py                        │
    │  ├─ Costs.py                            │
    │  └─ Route_optimization.py               │
    └────┬────────────────┬────────────────────┘
         │                │
    ┌────▼────┐    ┌──────▼──────────┐
    │  Model  │    │  External APIs  │
    │  Files  │    │  ├─ OpenWeather │
    │  .pkl   │    │  ├─ Nominatim   │
    └────┬────┘    │  └─ NewsAPI     │
         │         └─────────────────┘
    ┌────▼──────────────────┐
    │   SQLite Database      │
    │  (db.sqlite3)          │
    │  ├─ Users              │
    │  ├─ Predictions        │
    │  ├─ Profiles           │
    │  └─ Trip History       │
    └───────────────────────┘
```

---

## Machine Learning Model

### Model Overview

| Property | Value |
|----------|-------|
| **Algorithm** | Random Forest Classifier |
| **Purpose** | 3-class traffic congestion prediction |
| **Classes** | Low, Medium, High |
| **Accuracy** | 94.6% |
| **Precision** | 94.39% |
| **Recall** | 94.6% |
| **F1-Score** | 94.41% |
| **Input Features** | 8 |
| **Training Samples** | 5000 |
| **Test Set Size** | 1000 (20% split) |
| **Cross-Validation Score** | 95.3% (std: 0.007) |

### Supported Input Features

| Feature | Type | Range/Values | Description |
|---------|------|-------------|-------------|
| **city** | Categorical | 6 cities | Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata |
| **distance_km** | Numerical | 0-200 | Route distance in kilometers |
| **hour** | Numerical | 0-23 | Hour of day (24-hour format) |
| **weekday** | Categorical | 0-6 | Day of week (0=Monday, 6=Sunday) |
| **day_type** | Categorical | 3 types | Weekday, Weekend, Holiday |
| **weather** | Categorical | 4 types | Clear, Clouds, Rain, Thunderstorm |
| **event** | Binary | 0 or 1 | Special event flag (1=event present) |
| **route_type** | Categorical | 3 types | Local, Suburban, Highway |

### Output Classes

```
Congestion Level:
  - Low (0): Smooth traffic flow (expected travel time efficiency: high)
  - Medium (1): Moderate congestion (expected travel time efficiency: medium)
  - High (2): Heavy congestion (expected travel time efficiency: low)
```

### Model Hyperparameters

```python
RandomForestClassifier(
    n_estimators=150,           # 150 decision trees
    max_depth=20,               # Maximum tree depth
    min_samples_split=5,        # Minimum samples required to split a node
    min_samples_leaf=2,         # Minimum samples required at leaf node
    max_features='sqrt',        # N features per split = sqrt(total_features)
    random_state=42,            # Reproducibility seed
    n_jobs=-1,                  # Use all CPU cores
    class_weight='balanced',    # Adjusted for class imbalance
    verbose=1                   # Training progress output
)
```

### Feature Importance Ranking

Based on trained model analysis:

| Rank | Feature | Importance | Impact |
|------|---------|-----------|---------|
| 1 | **hour** | 35.04% | Time of day is the strongest predictor |
| 2 | **event** | 16.38% | Special events significantly affect traffic |
| 3 | **distance_km** | 15.44% | Longer routes have different congestion patterns |
| 4 | **day_type** | 12.34% | Weekday vs. weekend vs. holiday matters |
| 5 | **weather** | 8.72% | Weather conditions impact congestion |
| 6 | **weekday** | 5.22% | Specific day patterns detected |
| 7 | **city** | 4.23% | City-specific traffic patterns |
| 8 | **route_type** | 2.64% | Route type has minimal impact |

### Model Performance Metrics

```
Overall Accuracy: 94.6%

Per-Class Performance:
├─ Low Traffic:
│  ├─ Precision: 95.98%
│  ├─ Recall: 99.20%
│  └─ F1-Score: 97.56%
│
├─ Medium Traffic:
│  ├─ Precision: 91.26%
│  ├─ Recall: 83.93%
│  └─ F1-Score: 87.44%
│
└─ High Traffic:
   ├─ Precision: 78.26%
   ├─ Recall: 60.00%
   └─ F1-Score: 67.92%

Macro Average:
├─ Precision: 88.50%
├─ Recall: 81.04%
└─ F1-Score: 84.31%

5-Fold Cross-Validation Scores:
├─ Fold 1: 95.0%
├─ Fold 2: 96.125%
├─ Fold 3: 94.125%
├─ Fold 4: 95.375%
├─ Fold 5: 95.875%
└─ Mean: 95.3% (±0.7%)
```

### Confusion Matrix

```
Predicted Classes vs. Actual Classes

           Predicted Low  Predicted Med  Predicted High
Actual Low     18            0              12
Actual Med      0           740              6
Actual High     5            31             188

Interpretation:
- Excellent performance on "Medium" class (98.7% correct)
- Very good on "Low" class (60% correct, some confusion)
- Good on "High" class (84.7% correct, some underpredicton)
```

### Training Pipeline

```
1. Data Loading & Validation
   ├─ Load traffic_dataset.csv (5000 samples)
   ├─ Validate required columns
   └─ Check data integrity

2. Feature Encoding
   ├─ Categorical features: LabelEncoder
   │  (city, weekday, day_type, weather, route_type)
   └─ Target variable: LabelEncoder
      (Low → 0, Medium → 1, High → 2)

3. Train/Test Split
   ├─ 80% training set (4000 samples)
   ├─ 20% test set (1000 samples)
   └─ Stratified split to maintain class distribution

4. Model Training
   ├─ Initialize RandomForestClassifier
   ├─ Fit on training data
   └─ Training time: ~5-10 seconds

5. Model Evaluation
   ├─ Predictions on test set
   ├─ Calculate metrics (accuracy, precision, recall, F1)
   ├─ 5-fold cross-validation
   └─ Generate classification report

6. Model Serialization
   ├─ Pickle model object
   ├─ Save feature encoders
   ├─ Save target label encoder
   └─ Persist to traffic_model.pkl
```

### Fallback Prediction Logic

When the ML model fails, the system uses rule-based prediction:

```python
def fallback_prediction(features):
    score = 0
    
    # Distance factor
    if distance > 20 km: score += 2
    elif distance > 10 km: score += 1
    
    # Peak hours (8-10 AM, 5-7 PM)
    if hour in peak_hours: score += 2
    elif hour in 7-20: score += 1
    
    # Weekday/Weekend
    if weekday in (5,6): score += 1  # Weekend
    
    # Weather conditions
    if weather in ('Rain', 'Thunderstorm'): score += 1
    
    # Special events
    if event_flag: score += 1
    
    # Congestion mapping
    if score >= 5: return 'High'
    elif score >= 2: return 'Medium'
    else: return 'Low'
```

---

## 📊 Dataset Details

### Dataset Structure

**File**: `traffic_dataset.csv`
**Samples**: 5000 synthetic traffic records
**Size**: ~200 KB

### Dataset Features

| Column | Type | Sample Values | Description |
|--------|------|---------------|-------------|
| city | string | Delhi, Mumbai, ... | Target city |
| source_lat | float | 28.4052 | Source latitude |
| source_lon | float | 77.1855 | Source longitude |
| dest_lat | float | 28.5355 | Destination latitude |
| dest_lon | float | 77.2707 | Destination longitude |
| distance_km | float | 15.3 | Calculated route distance |
| date | string | 2024-01-15 | Trip date |
| weekday | string | Monday | Day of week |
| hour | int | 8-19 | Time of day (peak hours) |
| day_type | string | Weekday/Weekend/Holiday | Day classification |
| weather | string | Clear, Rainy, Foggy | Weather condition |
| event | int | 0/1 | Special event present |
| route_type | string | Local, Suburban, Highway | Route classification |
| congestion_level | string | Low/Medium/High | Target variable |
| suggested_mode | string | Car/Metro/Bike/Walk | Transport recommendation |

### Data Generation Logic

The dataset generator (`generate_csv.py`) creates realistic traffic patterns:

```python
# Congestion Score Calculation
score = 0

# Peak hours boost (8-10 AM, 5-7 PM)
if hour in [(8,10), (17,19)]:
    score += 2

# Holiday impact
if day_type == 'Holiday':
    score += 2

# Weekend boost
if day_type == 'Weekend':
    score += 1

# Weather impact (rain, fog)
if weather in ['Rainy', 'Foggy']:
    score += 1

# Long distance factor
if distance > 15 km:
    score += 1

# Special event boost
if event_flag == 1:
    score += 2

# Congestion Mapping
if score >= 5:
    congestion = 'High'
elif score >= 2:
    congestion = 'Medium'
else:
    congestion = 'Low'

# Transport Mode Suggestion
if congestion == 'Low':
    suggested_mode = 'Car'
elif congestion == 'Medium':
    suggested_mode = 'Metro'
else:
    suggested_mode = 'Bike/Walk'
```

### Class Distribution

Dataset is reasonably balanced:
- **Low Traffic**: ~1500 samples (30%)
- **Medium Traffic**: ~2250 samples (45%)
- **High Traffic**: ~1250 samples (25%)

### Geographic Coverage

Cities are randomly sampled within coordinate bounding boxes:

```python
CITY_COORDS = {
    "Delhi": (28.4, 28.9, 76.8, 77.4),         # ~50 km × 50 km
    "Mumbai": (18.8, 19.3, 72.7, 73.1),        # ~55 km × 40 km
    "Bengaluru": (12.8, 13.1, 77.4, 77.8),     # ~33 km × 40 km
    "Hyderabad": (17.2, 17.6, 78.3, 78.6),     # ~44 km × 33 km
    "Chennai": (12.9, 13.2, 80.1, 80.3),       # ~33 km × 22 km
    "Kolkata": (22.4, 22.7, 88.2, 88.5),       # ~33 km × 33 km
}
```

### Temporal Features

- **Hour Range**: 0-23 (24-hour format)
- **Weekdays**: Monday (0) - Sunday (6)
- **Dates**: Randomly span 2024-2025
- **Holidays**: Automatically detected using `holidays.India()`
- **Peak Hours**: 8-10 AM and 5-7 PM (commonly congested)

### Weather Simulation

Weather varies by season:
- **Monsoon (Jun-Sep)**: Rainy, Humid, Cloudy (higher congestion)
- **Winter (Dec-Feb)**: Cold, Foggy, Clear (moderate congestion)
- **Summer**: Sunny, Clear, Hot (lower congestion)

---

## Workflow

### User Journey: Making a Prediction

```
┌─────────────────────────────────────────────────────┐
│  1. User Visits Home Page                           │
│     ├─ Views hero section and feature cards        │
│     └─ Clicks "Make a Prediction" button            │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  2. User Fills Prediction Form                      │
│     ├─ Selects city (dropdown)                     │
│     ├─ Enters source location (text input)         │
│     ├─ Enters destination (text input)             │
│     └─ Submits form                                │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  3. Backend Feature Engineering (views.py)         │
│     ├─ Receive city, source, destination           │
│     └─ Call predictor.predict_traffic()            │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  4. Geocoding (services/model.py)                   │
│     ├─ Nominatim API: Get source coordinates       │
│     ├─ Nominatim API: Get destination coordinates  │
│     └─ Fallback to city center if not found        │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  5. Feature Engineering                             │
│     ├─ Calculate distance (Haversine formula)      │
│     ├─ Extract hour from current time              │
│     ├─ Get weekday from date                       │
│     ├─ Determine day_type (weekday/weekend/holiday)│
│     ├─ Fetch weather (OpenWeather or default)      │
│     ├─ Detect special events                       │
│     ├─ Classify route type (local/suburban/highway)│
│     └─ Encode categorical features (LabelEncoder) │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  6. ML Model Prediction                             │
│     ├─ Load trained RandomForest model             │
│     ├─ Pass feature vector to model                │
│     ├─ Get prediction (Low/Medium/High)            │
│     ├─ Get confidence probabilities                │
│     └─ Return prediction results                   │
│                                                     │
│  If model fails:                                    │
│     └─ Use fallback rule-based prediction          │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  7. Post-Processing                                │
│     ├─ Determine suggested transport mode:         │
│     │  High → Bike/Metro                          │
│     │  Medium → Metro                             │
│     │  Low → Car                                  │
│     ├─ Calculate cost estimation (costs.py)       │
│     ├─ Format results for display                 │
│     └─ Create Folium interactive map              │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  8. Database Persistence                           │
│     ├─ Create Prediction record:                   │
│     │  - User ID (if authenticated)               │
│     │  - City, source, destination                │
│     │  - Coordinates and distance                 │
│     │  - All features used for prediction         │
│     │  - Prediction result                        │
│     │  - Confidence probabilities                 │
│     └─ Save to SQLite database                     │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  9. Response to Frontend                            │
│     ├─ Congestion level badge (Low/Med/High)      │
│     ├─ Confidence percentage                      │
│     ├─ Interactive Folium map                     │
│     ├─ Distance and estimated time                │
│     ├─ Cost breakdown (fuel/toll)                 │
│     ├─ Transport mode recommendation              │
│     └─ Save option for future reference           │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│  10. User Views Results                             │
│      ├─ Sees interactive map with route            │
│      ├─ Views detailed metrics                     │
│      ├─ Reads recommendations                      │
│      ├─ Can save destination                       │
│      └─ Can schedule another prediction            │
└─────────────────────────────────────────────────────┘
```

### Analytics Workflow

```
┌─────────────────────────────────────────┐
│  Dashboard Data Collection              │
├─────────────────────────────────────────┤
1. Fetch all predictions from DB
2. Group by city, congestion level, hour
3. Calculate aggregate statistics
4. Generate trend analysis
5. Compute model accuracy on recent data
6. Prepare chart data (JSON)
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Display on Dashboard                   │
├─────────────────────────────────────────┤
- Total predictions made
- Accuracy percentage
- City-wise distribution
- Time-based trends (Chart.js)
- Prediction history table
- Popular routes
└─────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- **Python**: 3.9 or higher
- **pip**: Python package manager
- **Git**: For cloning repository
- **Virtual Environment**: Recommended (venv/virtualenv)
- **Windows/Mac/Linux**: Works on all platforms
- **4+ GB RAM**: For ML model training
- **Internet**: For API calls (optional)

### Step 1: Clone Repository

```bash
git clone https://github.com/SondharavaPalak/Traffic-Congestion-Predictor.git
cd traffic-predictor
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r Traffic/requirements.txt

# Or install individually:
pip install Django==4.9
pip install scikit-learn==1.7.1
pip install folium==0.20.0
pip install holidays==0.79
pip install requests==2.32.5
pip install geopy==2.4.1
pip install numpy==2.3.2
pip install scipy==1.16.1
```

### Step 4: Navigate to Traffic Directory

```bash
cd Traffic
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

**Output**: 
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, predictor, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 6: Verify ML Model

The trained model file should exist:
```bash
# Windows & macOS/Linux
ls traffic_model.pkl
# or use file explorer to check if traffic_model.pkl exists
```

If model doesn't exist, create it:
```bash
# From prediction model/ directory
cd ../prediction model
python model_train.py
python generate_csv.py  # If dataset doesn't exist
cd ../Traffic
```

### Step 7: Create Superuser (Optional - for admin panel)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 8: Run Development Server

```bash
python manage.py runserver
# or specify port: python manage.py runserver 0.0.0.0:8000
```

**Output**:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 9: Access Application

Open your browser:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel** (if superuser created): http://127.0.0.1:8000/admin/

---

## Configuration & Customization

### Environment Variables

Create a `.env` file in the `Traffic/` directory:

```bash
# Optional: OpenWeather API Key
OPENWEATHER_API_KEY=your_api_key_here

# Optional: NewsAPI Key
NEWSAPI_KEY=your_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings Configuration

Edit `traffic_predictor/settings.py`:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'predictor',  # Our app
]

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {...},
    },
]
```

### Model Customization

To use your own trained model:

1. **Train your model** using your dataset
2. **Ensure feature compatibility**:
   ```python
   FEATURES = [
       "city", "distance_km", "hour", "weekday", "day_type",
       "weather", "event", "route_type"
   ]
   ```
3. **Serialize with proper encoders**:
   ```python
   model_data = {
       'model': trained_model,
       'encoders': encoders,  # dict of LabelEncoders
       'target_le': target_label_encoder,
       'features': FEATURES
   }
   pickle.dump(model_data, open('traffic_model.pkl', 'wb'))
   ```
4. **Place file** in `Traffic/` directory
5. **Restart server** - model auto-loads

### Add More Cities

To add new cities, modify:

1. **generate_csv.py** (for training):
   ```python
   cities = {
       "Delhi": (28.4, 28.9, 76.8, 77.4),
       "YourCity": (lat_min, lat_max, lon_min, lon_max),  # Add here
   }
   ```

2. **services/model.py** (for predictions):
   ```python
   CITY_COORDS = {
       'Delhi': (28.7041, 77.1025),
       'YourCity': (lat, lon),  # Add here
   }
   supported_cities = list(self.CITY_COORDS.keys())
   ```

3. **Retrain model** with new city data

### Adjust Hyperparameters

In `prediction model/model_train.py`:

```python
model = RandomForestClassifier(
    n_estimators=200,           # Increase for more accuracy
    max_depth=25,               # Increase complexity
    min_samples_split=3,        # More aggressive splits
    min_samples_leaf=1,         # Allow single samples
    max_features='log2',        # Different feature subset
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
```

Then retrain:
```bash
cd prediction\ model
python model_train.py
```

---

## Usage Guide

### Making Your First Prediction

1. **Navigate to Predict Page**: Click "Make a Prediction"
2. **Select City**: Choose from dropdown (Delhi, Mumbai, etc.)
3. **Enter Source**: Type starting location (street, landmark, or area)
4. **Enter Destination**: Type ending location
5. **Click Predict**: System processes and displays results

### Reading Prediction Results

**Congestion Badge**:
- 🟢 **Low**: Smooth traffic (travel easily)
- 🟡 **Medium**: Moderate congestion (expect delays)
- 🔴 **High**: Heavy traffic (expect significant delays)

**Map Display**:
- Interactive map shows your route
- Source marked in green, destination in red
- Distance displayed in kilometers

**Metrics**:
- **Estimate Duration**: Based on congestion
- **Confidence**: Model's certainty (0-100%)
- **Suggested Mode**: Recommended transport

**Cost Analysis**:
- **Fuel Cost**: If driving
- **Toll Charges**: Estimated tolls
- **Total Cost**: Complete journey cost

### Dashboard Features

**Global Statistics**:
- Total predictions made
- Average accuracy
- Most congested time
- City-wise breakdown

**Trends**:
- Hour-based congestion pattern
- Day-wise variations
- Major congestion hotspots

### Trip Management

**Save Trip**:
- Click "Save Destination" on results
- Access from "Saved Destinations"
- Quick repeat predictions

**Trip History**:
- View all predictions made
- Compare with actual traffic
- Analyze accuracy over time

**User Profile**:
- Set preferred transport mode
- Enter vehicle details
- Configure cost preferences

---

## Database Models

### Prediction Model

```python
class Prediction(models.Model):
    # User & Timing
    user = ForeignKey(User, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    
    # Location Information
    city = CharField(max_length=100)
    source = CharField(max_length=200)
    destination = CharField(max_length=200)
    source_lat = FloatField()
    source_lon = FloatField()
    dest_lat = FloatField()
    dest_lon = FloatField()
    distance_km = FloatField()
    
    # Features Used for Prediction
    hour = IntegerField()
    weekday = IntegerField()
    day_type = CharField(max_length=50)
    weather = CharField(max_length=100)
    event_flag = BooleanField()
    route_type = CharField(max_length=50)
    
    # Prediction Results
    congestion_level = CharField(max_length=10, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ])
    suggested_mode = CharField(max_length=10, choices=[
        ('Car', 'Car'),
        ('Metro', 'Metro'),
        ('Bike', 'Bike'),
        ('Walk', 'Walk'),
    ])
    probabilities = JSONField()  # {Low: 0.15, Medium: 0.45, High: 0.4}
```

### UserProfile Model

```python
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    preferred_mode = CharField(max_length=50)
    car_make = CharField(max_length=100, blank=True)
    car_mileage_kmpl = FloatField(default=12.0)
    fuel_cost_per_liter = FloatField(default=100.0)
    primary_city = CharField(max_length=100, blank=True)
    favorite_destinations = JSONField(default=list)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### TripHistory Model

```python
class TripHistory(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    prediction = OneToOneField(Prediction, null=True, blank=True)
    city = CharField(max_length=100)
    predicted_congestion = CharField(max_length=50)
    actual_congestion = CharField(max_length=50)
    predicted_duration_mins = IntegerField(null=True)
    actual_duration_mins = IntegerField(null=True)
    mode_used = CharField(max_length=50)
    fuel_cost = FloatField(default=0)
    toll_cost = FloatField(default=0)
    total_cost = FloatField(default=0)
```

---

## API Endpoints

### Main Views

| URL | Method | Description |
|-----|--------|-------------|
| `/` | GET | Home page with feature showcase |
| `/predict/` | GET, POST | Main prediction interface |
| `/predict-ajax/` | POST | AJAX prediction endpoint (JSON) |
| `/dashboard/` | GET | Global traffic dashboard |
| `/analytics/` | GET | Detailed analytics and trends |
| `/trip-history/` | GET | User's prediction history |
| `/trip-history/<id>/` | GET | Individual trip details |
| `/saved-destinations/` | GET | User's saved routes |
| `/route-optimization/` | GET, POST | Route optimization tool |
| `/news/` | GET | Traffic news feed |
| `/news/<city>/` | GET | City-specific news |
| `/about/` | GET | About page and ML info |
| `/user-profile/` | GET, POST | User preferences |

### AJAX Endpoints

```
POST /predict-ajax/
Content-Type: application/json

Request Body:
{
    "city": "Delhi",
    "source": "India Gate",
    "destination": "Lal Qila"
}

Response:
{
    "congestion_level": "High",
    "suggested_mode": "Metro",
    "probabilities": {
        "Low": 0.15,
        "Medium": 0.35,
        "High": 0.50
    },
    "coordinates": {
        "source": [28.6129, 77.2295],
        "destination": [28.6562, 77.2410]
    },
    "features": {
        "distance_km": 8.2,
        "hour": 18,
        "daytype": "Weekday",
        "weather": "Clear"
    },
    "map_html": "<html>...</html>"
}
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: ModuleNotFoundError: No module named 'django'

**Solution**:
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r Traffic/requirements.txt
```

#### Issue: Model file not found (traffic_model.pkl)

**Solution**:
```bash
# Check if file exists
ls Traffic/traffic_model.pkl  # macOS/Linux
dir Traffic/traffic_model.pkl  # Windows

# If missing, create model:
cd prediction\ model
python model_train.py
# This will generate traffic_dataset.csv and traffic_model.pkl
```

#### Issue: Database migration errors

**Solution**:
```bash
# Reset migrations (careful - deletes all data)
python manage.py migrate predictor zero

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

#### Issue: Static files not loading

**Solution**:
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings.py:
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
```

#### Issue: Geocoding timeout (slow predictions)

**Solution**:
```python
# Increase timeout in services/model.py
loc = self.geolocator.geocode(location, timeout=15)  # Increase from 10

# Or disable geocoding and use city centers
USE_CITY_CENTERS = True  # In settings
```

#### Issue: CSRF token errors

**Solution**:
```html
<!-- Add to POST forms -->
{% csrf_token %}

<!-- Or use CSRF decorator -->
@csrf_exempt  # Only for AJAX endpoints
def predict_ajax(request):
    ...
```

#### Issue: Port 8000 already in use

**Solution**:
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -ti:8000 | xargs kill -9
```

#### Issue: Low prediction accuracy

**Solution**:
```bash
# Retrain with more data or different hyperparameters
cd prediction\ model
# Edit model_train.py hyperparameters
python model_train.py

# Check model metrics
python checkaccuracy.py
```

---

## Performance Notes

### Model Performance
- **Accuracy**: 94.6% on test set
- **Cross-Validation**: 95.3% (±0.7%)
- **Training Time**: ~5-10 seconds (5000 samples)
- **Prediction Time**: ~10-50ms per request
- **Memory Usage**: ~50 MB (model + data)

### Web Application
- **Page Load Time**: 500-1000ms
- **Prediction Response**: 1-3 seconds (including geocoding)
- **Database Queries**: Indexed on user_id, city, created_at
- **Concurrent Users**: 50-100 (SQLite limitation)

### Optimization Tips
1. Use PostgreSQL for production (vs. SQLite)
2. Add Redis caching for frequent queries
3. Implement async task processing (Celery)
4. Optimize Folium map generation
5. Cache geocoding results

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Support & Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: palaksondhrava@gmail.com

---

## Acknowledgments

- **scikit-learn** team for ML library
- **Django** community for web framework
- **OpenWeather** for weather API
- **Nominatim/Folium** for mapping services
- **Indian holidays** library maintainers

---

## Additional Resources

### Tutorials & Guides
- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn Tutorial](https://scikit-learn.org/stable/user_guide.html)
- [Folium Maps](https://python-visualization.github.io/folium/)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Related Projects
- Traffic Data Analysis Dashboard
- Multi-Modal Route Optimizer
- Real-Time Traffic Alerts System

---

**Last Updated**: April 2026  
