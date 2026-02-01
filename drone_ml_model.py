import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load dataset
path = r"C:\Users\HIMESH KRISHNA\OneDrive\Attachments\Desktop\Supplemental Drone Telemetry Data - Drone Operations Log.csv"
df = pd.read_csv(path, engine="python", on_bad_lines="skip")

# Select needed columns
df = df[
    [
        "Altitude (meters)",
        "Flight Duration (minutes)",
        "Distance Flown (km)",
        "Actual Carry Weight (kg)",
        "Wind Speed (m/s)",
        "Battery Remaining (%)"
    ]
]

# Drop missing values
df = df.dropna()

# Split features and target
X = df.drop("Battery Remaining (%)", axis=1)
y = df["Battery Remaining (%)"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# SAVE THE TRAINED MODEL HERE
import joblib
joblib.dump(model, "drone_battery_model.pkl")
print("Model saved successfully!")

# Evaluate model
preds = model.predict(X_test)
error = mean_absolute_error(y_test, preds)

print("Model trained successfully!")
print("Mean Absolute Error:", error)

# Test sample prediction
sample = pd.DataFrame([[120, 15, 3.5, 2.0, 5.0]], columns=X.columns)
prediction = model.predict(sample)
print("Predicted Battery Remaining:", prediction[0], "%")
