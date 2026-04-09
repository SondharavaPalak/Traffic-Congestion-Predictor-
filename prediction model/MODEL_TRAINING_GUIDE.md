# Model Training Guide - Traffic Predictor

## 📊 Machine Learning Model Documentation

### Model Overview

**Model Type:** Random Forest Classifier  
**Purpose:** 3-class traffic congestion prediction (Low, Medium, High)  
**Input Features:** 8  
**Output Classes:** 3  
**Training Data:** 5000 synthetic samples  
**Version:** 2.0 (Professional)  

---

## 🗂️ Training Data Structure

### Dataset Features

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `city` | categorical | 6 cities | Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata |
| `distance_km` | numerical | 0-200 | Route distance in kilometers |
| `hour` | numerical | 0-23 | Hour of day |
| `weekday` | categorical | 0-6 | 0=Mon, 6=Sun |
| `day_type` | categorical | 3 types | Weekday, Weekend, Holiday |
| `weather` | categorical | 4 types | Clear, Clouds, Rain, Thunderstorm |
| `event` | binary | 0-1 | Special event flag |
| `route_type` | categorical | 3 types | Local, Suburban, Highway |

### Target Variable

```
congestion_level:
  - Low: 0 (smooth traffic)
  - Medium: 1 (moderate congestion)
  - High: 2 (heavy congestion)
```

### Data Generation Logic

Located in: `generate_csv.py`

**Congestion Scoring Algorithm:**
```python
score = 0

# Peak hours (8-10 AM, 5-7 PM): +2
if hour in [(8-10), (17-19)]:
    score += 2

# Holiday/Special Event: +2
if day_type == 'Holiday':
    score += 2

# Weekend: +1
if day_type == 'Weekend':
    score += 1

# Bad weather (Rain/Fog): +1
if weather in ['Rain', 'Thunderstorm']:
    score += 1

# Long distance (>15km): +1
if distance > 15:
    score += 1

# Congestion mapping:
if score >= 5: congestion = 'High'
elif score >= 2: congestion = 'Medium'
else: congestion = 'Low'
```

---

## 🤖 Model Hyperparameters (v2.0)

### Optimized Configuration

```python
RandomForestClassifier(
    n_estimators=150,           # Number of trees
    max_depth=20,               # Tree depth limit
    min_samples_split=5,        # Min samples to split (from 2)
    min_samples_leaf=2,         # Min samples per leaf (from 1)
    max_features='sqrt',        # Features per split
    random_state=42,            # Reproducibility
    n_jobs=-1,                  # All CPU cores
    class_weight='balanced',    # Handle class imbalance
)
```

### Hyperparameter Justification

| Parameter | Old | New | Reason |
|-----------|-----|-----|--------|
| `n_estimators` | 100 | 150 | More trees = better generalization |
| `max_depth` | None | 20 | Prevent overfitting on training data |
| `min_samples_split` | 2 | 5 | Require more evidence for splits |
| `min_samples_leaf` | 1 | 2 | Prevent single-sample leaves (noise) |
| `class_weight` | None | balanced | Handle 3-class imbalance |

---

## 📈 Training Process

### Step-by-Step Execution

```bash
# 1. Navigate to model directory
cd prediction\ model

# 2. Generate synthetic dataset
python generate_csv.py
# Creates: traffic_dataset.csv (5000 rows)

# 3. Train model
python model_train.py
# Creates: traffic_model.pkl, model_metrics.json

# 4. Evaluate accuracy
python checkaccuracy.py
# Shows: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
```

### Model Training Output

The training script (`model_train.py` v2.0) now produces:

**Console Output:**
```
====================================================
MODEL PERFORMANCE METRICS
====================================================
Accuracy: 0.8340
Precision (weighted): 0.8245
Recall (weighted): 0.8340
F1 Score (weighted): 0.8267
Cross-Validation Accuracy: 0.8122 (+/- 0.0234)

Feature Importance (Top 5):
  hour: 0.2845
  distance_km: 0.2134
  weekday: 0.1876
  weather: 0.1432
  day_type: 0.0987
====================================================
✓ Model saved as 'traffic_model.pkl'
✓ Metrics saved as 'model_metrics.json'
```

**Generated Files:**
- `traffic_model.pkl` - Model package (contains model, encoders, metadata)
- `model_metrics.json` - Performance metrics and statistics

---

## 🔍 Model Metrics Explained

### Key Metrics

**Accuracy:** Overall correctness
- Formula: (TP + TN) / (TP + TN + FP + FN)
- Expected: 75-85%

**Precision:** Correctness when predicting a class
- Formula: TP / (TP + FP)
- High precision = Few false positives

**Recall:** Coverage of actual instances
- Formula: TP / (TP + FN)
- High recall = Few false negatives

**F1-Score:** Harmonic mean of precision & recall
- Formula: 2 * (Precision * Recall) / (Precision + Recall)
- Balanced metric between precision and recall

**Cross-Validation:** Robustness across data splits
- 5-fold by default
- Helps detect overfitting

### Confusion Matrix Interpretation

```
                 Predicted
              Low  Medium High
Actual Low     45     8      2    (55 samples)
       Medium   6    38      4    (48 samples)
       High     2     5     40    (47 samples)

Diagonal = Correct predictions
Off-diagonal = Misclassifications
```

---

## 🔧 Feature Engineering

### Feature Transformation

**Categorical Features (Label Encoded):**
- `city`: 6 classes → {0, 1, 2, 3, 4, 5}
- `weekday`: 7 classes → {0, 1, 2, 3, 4, 5, 6}
- `day_type`: 3 classes → {Holiday, Weekday, Weekend}
- `weather`: 4 classes → {Clear, Clouds, Rain, Thunderstorm}
- `route_type`: 3 classes → {local, suburban, highway}

**Numerical Features (No scaling needed for Random Forest):**
- `distance_km`: 0-200 km (continuous)
- `hour`: 0-23 (discrete, normalized by model tree structure)
- `event`: 0-1 (binary)

### Feature Importance

Random Forest calculates importance by measuring how much each feature decreases impurity (Gini importance):

**Expected Rankings:**
1. `hour` (20-30%) - Peak hours dominate congestion
2. `distance_km` (15-25%) - Long routes problematic
3. `weekday` (12-18%) - Day patterns matter
4. `weather` (10-15%) - Weather impacts traffic
5. `day_type` (8-12%) - Holidays/weekends differ
6. `event` (5-10%) - Events cause spikes
7. `city` (5-10%) - City differences minor
8. `route_type` (2-8%) - Route type least important

---

## ⚠️ Common Issues & Solutions

### Issue 1: Low Model Accuracy (<70%)

**Cause:** Data imbalance or poor feature engineering

**Solution:**
```python
# Increase training data
df = generate_data(n=10000)  # Instead of 5000

# Adjust hyperparameters
RandomForestClassifier(
    n_estimators=200,      # More trees
    max_depth=25,          # Allow deeper trees
    min_samples_split=3,   # Lower this value
)
```

### Issue 2: Overfitting (Train Acc >> Test Acc)

**Cause:** Model memorizing training data

**Solution:**
```python
# Reduce model complexity
RandomForestClassifier(
    n_estimators=100,      # Fewer trees
    max_depth=15,          # Shallower trees
    min_samples_split=10,  # Higher value
    min_samples_leaf=5,    # Higher value
)
```

### Issue 3: Class Imbalance

**Cause:** Unequal distribution between Low/Medium/High

**Solution:**
```python
# Already enabled in v2.0
RandomForestClassifier(
    class_weight='balanced',  # Adjust weights automatically
)

# Or manual weights
class_weight={
    'Low': 1.0,
    'Medium': 1.2,
    'High': 1.5
}
```

---

## 🚀 Production Model Management

### Model Versioning

Save model versions with timestamp:

```python
import time
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = f"traffic_model_v{timestamp}.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model_package, f)
```

### Model Monitoring

Track performance over time:

```python
# Retrain periodically with new data
# Compare new model metrics with previous version
# Alert if accuracy drops >5%
```

### Model Updates

```python
# Periodic retraining schedule:
# - Weekly: If new data available
# - Monthly: Automatic batch retraining
# - Quarterly: Major version updates

# Always test before production deployment
```

---

## 📚 Advanced Improvements (Future)

### 1. Feature Engineering Enhancements

```python
# Cyclical encoding for hour/weekday
hour_sin = np.sin(2 * np.pi * hour / 24)
hour_cos = np.cos(2 * np.pi * hour / 24)

# Lag features (previous hour congestion)
features['congestion_lag_1h'] = previous_hour_congestion

# Rolling statistics
features['distance_7d_avg'] = rolling_avg_distance
```

### 2. Advanced Models

```python
# XGBoost
from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=150, max_depth=7)

# LightGBM
from lightgbm import LGBMClassifier
model = LGBMClassifier(n_estimators=150, max_depth=15)

# Neural Networks
from sklearn.neural_network import MLPClassifier
model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500)
```

### 3. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [10, 15, 20, 25],
    'min_samples_split': [2, 5, 10],
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1_weighted'
)
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_}")
```

### 4. Integration with Real Data

```python
# Connect to traffic APIs
# - Google Maps Platform (real-time traffic)
# - City traffic departments
# - Private traffic data providers

# Continuous learning pipeline
# - Collect predictions vs actual outcomes
# - Retrain weekly with new data
# - Monitor model drift
```

---

## 📞 Training Support

For issues during training:
1. Check logs in `logs/model_training.log`
2. Review dataset in `traffic_dataset.csv`
3. Check metrics in `model_metrics.json`
4. Verify model size: `ls -lh traffic_model.pkl`

**Expected model file size:** 2-10 MB

---

**Last Updated:** April 7, 2026  
**Version:** 2.0 (Professional Edition)
