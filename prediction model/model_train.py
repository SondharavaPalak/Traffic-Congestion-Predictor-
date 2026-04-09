"""
Traffic Congestion Prediction Model Training
============================================

This module trains a Random Forest classifier to predict traffic congestion levels.

Model Details:
- Algorithm: Random Forest Classifier
- Features: 8 (city, distance_km, hour, weekday, day_type, weather, event, route_type)
- Target Classes: 3 (Low, Medium, High)
- Data Size: 5000 samples
- Train/Test Split: 80/20

Author: Traffic Predictor Team
Version: 2.0
"""

import pandas as pd
import numpy as np
import pickle
import json
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def train_model() -> dict:
    """
    Train Random Forest model for traffic congestion prediction.
    
    Returns:
        dict: Contains model, encoders, target encoder, and metrics
        
    Raises:
        FileNotFoundError: If dataset file not found
        ValueError: If dataset is empty or invalid
    """
    logger.info("Starting model training pipeline...")
    
    try:
        # Load dataset
        logger.info("Loading dataset...")
        df = pd.read_csv("traffic_dataset.csv")
        
        if df.empty:
            raise ValueError("Dataset is empty")
        
        logger.info(f"Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
        
        # Validate dataset
        required_columns = [
            "city", "distance_km", "hour", "weekday", "day_type",
            "weather", "event", "route_type", "congestion_level"
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Encode categorical features
        logger.info("Encoding categorical features...")
        encoders = {}
        categorical_features = ["city", "weekday", "day_type", "weather", "route_type"]
        
        for col in categorical_features:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            logger.info(f"  Encoded {col}: {len(le.classes_)} classes")
        
        # Prepare features and target
        feature_names = [
            "city", "distance_km", "hour", "weekday", "day_type",
            "weather", "event", "route_type"
        ]
        
        X = df[feature_names]
        y_raw = df["congestion_level"]
        
        # Encode target variable
        logger.info("Encoding target variable...")
        target_le = LabelEncoder()
        y = target_le.fit_transform(y_raw)
        
        logger.info(f"  Target classes: {target_le.classes_}")
        logger.info(f"  Class distribution:\n{pd.Series(y_raw).value_counts()}")
        
        # Train/test split
        logger.info("Splitting dataset (80/20)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"  Training set: {X_train.shape[0]} samples")
        logger.info(f"  Test set: {X_test.shape[0]} samples")
        
        # Train Random Forest with optimized hyperparameters
        logger.info("Training Random Forest Classifier...")
        model = RandomForestClassifier(
            n_estimators=150,           # Increased for better accuracy
            max_depth=20,               # Prevent overfitting
            min_samples_split=5,        # Require more samples to split
            min_samples_leaf=2,         # Require minimum leaves
            max_features='sqrt',        # Use sqrt of features
            random_state=42,            # Reproducibility
            n_jobs=-1,                  # Use all CPU cores
            class_weight='balanced',    # Handle class imbalance
            verbose=1
        )
        
        model.fit(X_train, y_train)
        logger.info("Model training completed!")
        
        # Make predictions
        logger.info("Evaluating model performance...")
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            "f1_score": float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classification_report": classification_report(
                y_test, y_pred,
                target_names=target_le.classes_,
                output_dict=True
            )
        }
        
        # Cross-validation
        logger.info("Performing 5-fold cross-validation...")
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        metrics["cross_val_scores"] = cv_scores.tolist()
        metrics["cross_val_mean"] = float(cv_scores.mean())
        metrics["cross_val_std"] = float(cv_scores.std())
        
        # Feature importance
        logger.info("Calculating feature importance...")
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        metrics["feature_importance"] = feature_importance.to_dict('records')
        
        # Log metrics
        logger.info("=" * 60)
        logger.info("MODEL PERFORMANCE METRICS")
        logger.info("=" * 60)
        logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"Precision (weighted): {metrics['precision']:.4f}")
        logger.info(f"Recall (weighted): {metrics['recall']:.4f}")
        logger.info(f"F1 Score (weighted): {metrics['f1_score']:.4f}")
        logger.info(f"Cross-Validation Accuracy: {metrics['cross_val_mean']:.4f} (+/- {metrics['cross_val_std']:.4f})")
        logger.info("\nFeature Importance (Top 5):")
        for idx, row in feature_importance.head(5).iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        logger.info("=" * 60)
        
        # Prepare model package
        model_package = {
            "model": model,
            "encoders": encoders,
            "target_le": target_le,
            "metrics": metrics,
            "feature_names": feature_names,
            "training_date": datetime.now().isoformat(),
            "model_version": "2.0"
        }
        
        # Save model
        logger.info("Saving model package...")
        with open("traffic_model.pkl", "wb") as f:
            pickle.dump(model_package, f)
        logger.info("✓ Model saved as 'traffic_model.pkl'")
        
        # Save metrics
        logger.info("Saving metrics report...")
        with open("model_metrics.json", "w") as f:
            # Convert non-serializable objects
            metrics_copy = metrics.copy()
            if "classification_report" in metrics_copy:
                metrics_copy["classification_report"] = str(metrics_copy["classification_report"])
            json.dump(metrics_copy, f, indent=2)
        logger.info("✓ Metrics saved as 'model_metrics.json'")
        
        logger.info("Model training pipeline completed successfully!")
        return model_package
        
    except FileNotFoundError as e:
        logger.error(f"Dataset file not found: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during training: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        exit(1)

