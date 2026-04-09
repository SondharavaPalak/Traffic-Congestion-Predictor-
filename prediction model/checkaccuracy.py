import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the saved model and encoders
data = pickle.load(open("traffic_model.pkl", "rb"))
model = data["model"]
encoders = data["encoders"]
target_le = data["target_le"]

# Load dataset again (same one you trained on)
df = pd.read_csv("traffic_dataset.csv")

# Apply encoders to categorical columns
for col, le in encoders.items():
    df[col] = le.transform(df[col])

# Features & target
X = df[["city","distance_km","hour","weekday","day_type","weather","event","route_type"]]
y = target_le.transform(df["congestion_level"])

# Split dataset (same as training)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Detailed report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_le.classes_))

# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
