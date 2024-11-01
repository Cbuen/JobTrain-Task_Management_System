import pandas as pd

# Define task categories and examples
categories = {
    'Fitness': [
        'go to gym', 'morning yoga session', 'evening run', 'walking the dog', 'attend fitness class',
        'swimming session', 'cycling', 'hiking', 'weight lifting', 'aerobics class'
    ],
    'Bills': [
        'pay electricity bill', 'pay gym membership', 'pay rent', 'pay credit card bill', 'pay water bill',
        'pay internet bill', 'pay phone bill', 'pay insurance premium', 'pay mortgage', 'pay loan installment'
    ],
    'Health': [
        'annual health checkup', 'dentist appointment', 'doctor appointment', 'meditate for 20 minutes', 'buy vitamins',
        'yoga session', 'therapy session', 'buy prescription medicine', 'health insurance renewal', 'get flu shot'
    ],
    'Work': [
        'team meeting at 2 PM', 'submit project report', 'attend conference call', 'finish coding assignment', 'weekly team sync',
        'prepare presentation', 'client meeting', 'review team performance', 'update project plan', 'send weekly updates'
    ],
    'Errands': [
        'buy groceries', 'pick up dry cleaning', 'post office visit', 'car maintenance', 'bank visit',
        'buy pet food', 'drop off recycling', 'pick up kids from school', 'buy birthday gift', 'return library books'
    ],
    'Personal Development': [
        'read a book', 'take an online course', 'practice a new language', 'attend a workshop', 'write in journal',
        'learn to play an instrument', 'practice coding', 'meditation session', 'watch educational videos', 'work on a hobby'
    ],
    'Social': [
        'call a friend', 'attend a social event', 'go out for dinner', 'visit family', 'plan a party',
        'join a club', 'volunteer at a local charity', 'attend a concert', 'go to a movie', 'host a game night'
    ]
}

# Convert the dictionary to a list of task-category pairs
data = []
for category, tasks in categories.items():
    for task in tasks:
        data.append({'Task': task.lower(), 'Category': category})  # Convert tasks to lowercase here

# Create a DataFrame
df = pd.DataFrame(data)

# Validate column names and check for missing values
if list(df.columns) == ['Task', 'Category']:
    print("Column names are correct.")
else:
    print("Column names are incorrect:", df.columns)

# Check for missing values
if df.isnull().sum().sum() == 0:
    print("No missing values found.")
else:
    print("Missing values detected. Details:\n", df.isnull().sum())

# Save the DataFrame to a CSV file
df.to_csv('task_data.csv', index=False)
print("Data saved to 'task_data.csv'")
