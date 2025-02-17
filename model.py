"""
Data fields
N - ratio of Nitrogen content in soil
P - ratio of Phosphorous content in soil
K - ratio of Potassium content in soil
temperature - temperature in degree Celsius
humidity - relative humidity in %
ph - ph value of the soil
rainfall - rainfall in mm
month - best month for sowing
"""

print('DATA INFO')

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv('Crop_recommendation.csv')
# Encode categorical variables
encoder = LabelEncoder()
encoder.fit_transform([
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"])
df['month'] = encoder.transform(df['month'])

print(df.shape)
y = df['label'].values
df_X = df.drop(['label'],axis=1)
df_X.head()


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df_X, y, test_size=0.2, random_state=42,stratify=y)

# Random Forest model
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Model evaluation
accuracy = classifier.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")


# Save the model & encoders
with open("model.pkl", "wb") as f:
    pickle.dump({"model": classifier, "encoders": encoder}, f)
