import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Load and preprocess the data
df = pd.read_csv('task_data.csv')
df['Task'] = df['Task'].str.lower()  # Convert all tasks to lowercase

# Encode categories
le = LabelEncoder()
df['Category'] = le.fit_transform(df['Category'])

# Balance the dataset
min_samples = df['Category'].value_counts().min()
df_balanced = df.groupby('Category').apply(lambda x: x.sample(min_samples)).reset_index(drop=True)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(df_balanced['Task'], df_balanced['Category'], test_size=0.2, random_state=42)

# Create a pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', SVC(probability=True)),
])

# Define parameters for GridSearchCV
parameters = {
    'tfidf__max_df': (0.5, 0.75, 1.0),
    'tfidf__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    'clf__C': (0.1, 1, 10),
    'clf__kernel': ('linear', 'rbf'),
}

# Perform GridSearchCV
grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

# Evaluate the model
y_pred = grid_search.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Function to predict categories
def predict_category(tasks):
    tasks = [task.lower() for task in tasks]  # Convert to lowercase
    predicted_categories = grid_search.predict(tasks)
    return [le.inverse_transform([cat])[0] for cat in predicted_categories]
