import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('Crop_recommendation.csv')
print(df.shape)
df.head()

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

pickle.dump(classifier,open("model.pkl","wb"))
