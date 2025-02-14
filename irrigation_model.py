import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv("rice_irrigation_UP.csv")

# Encode categorical variables
label_encoders = {}
for col in ["Soil_Type", "Crop_Stage", "Irrigation_Needed"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features (X) and target (y)
X = df.drop(columns=["Date", "State", "Irrigation_Needed"])
y = df["Irrigation_Needed"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

# Train Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the model & encoders
with open("irrigation_model.pkl", "wb") as f:
    pickle.dump({"model": rf_model, "encoders": label_encoders}, f)


# Model evaluation
accuracy = rf_model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")
print("Model saved successfully!")
