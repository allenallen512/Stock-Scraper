from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Assuming you have a dataset loaded into a pandas DataFrame called 'data'
# and the target variable is named 'label'

# Split the dataset into features (X) and target (y)
X = data.drop(columns=['label'])
y = data['label']

# Print out each individual header
print("Features (X) headers:")
for header in X.columns:
    print(header)

print("\nTarget (y) header:")
print(y.name)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
