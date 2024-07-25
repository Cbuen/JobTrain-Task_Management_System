import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report



df = pd.read_csv('task_data.csv')

# Preprocess the data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['task'])
y = df['category']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = MultinomialNB()
model.fit(X_train, y_train)


"""
Used for testing purposes in evaluating the models data-set
"""

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy}')

# # Print detailed classification report
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))



# Example prediction for multiple tasks
new_tasks = ["final project school"]

# creatred the model now need to take the model and integrate with my gui 

def predict_category(tasks):
    if tasks:
        new_tasks_transformed = vectorizer.transform(tasks)
        predicted_categories = model.predict(new_tasks_transformed)

        for task, category in zip(tasks, predicted_categories):
            print(f'Task: {task}, Predicted Category: {category}')