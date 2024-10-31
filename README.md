# Task Management System with NLP-based Task Categorization
**Final Project for Google IT Automation Class via Job Train**

This repository contains a task management system implemented using Python and PyQt5. The system provides a user-friendly graphical user interface (GUI) for managing tasks, including adding new tasks, viewing existing tasks, and marking tasks as completed. It also includes a Natural Language Processing (NLP) model to categorize tasks automatically.

## Features

- Add New Task: Easily add new tasks to the system using a dialog window.
- View Tasks: View the list of tasks in a separate dialog window.
- Complete Task: Mark tasks as completed from a dialog window.
- Exit Confirmation: When attempting to exit the application, a confirmation dialog prompts the user for confirmation.
**Added Features**
- Automatic Task Categorization: Uses an NLP model to categorize tasks based on their descriptions.
- Organized Task View: View tasks grouped by their assigned categories.
- Save and Load Tasks: Save tasks to a JSON file and load them when the application restarts.
- Live Clock: Displays the current date and time, updated every minute.
  
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
  <img width="48%" alt="Task-manager-1" src="https://github.com/user-attachments/assets/52287520-372d-4262-80a9-ddd27c89a7ba">
  <img width="48%" alt="Task-manager-2" src="https://github.com/user-attachments/assets/e472d53d-2732-4b91-a937-28feeaf12997">
  <img width="48%" alt="Task-manager-3" src="https://github.com/user-attachments/assets/90fbb579-faeb-473a-bcb6-77d8ba838867">
  <img width="48%" alt="Task-manager-4" src="https://github.com/user-attachments/assets/03f48142-95d7-4d3b-b0df-c138b3a920c4">
</div>

## Getting Started

To run the task management system locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/usman010803/Task_Management_System.git
```

2. Navigate to the project directory:

```bash
cd Task_Management_System
```

3. Install the required dependencies. Ensure that you have Python and PyQt5 installed.

```bash
pip install pyqt5
```

4. Run the application:

```bash
python task_management_system.py
```

## Usage

Upon launching the application, a main window will appear, providing access to various functionalities:

- Click the "Add New Task" button to add a new task.
- Click the "View Tasks" button to view the list of tasks.
- Click the "Organized Task View" button to see tasks grouped by categories. (post to generating them)
- Click the "Generate your task categories" button to categorize tasks using the NLP model.
- Click the "Complete Task" button to mark a task as completed.
- Click the "Save" button to save tasks to a JSON file.
- Click the "Clean Save" button to overwrite existing saved tasks.
- Click the "Exit" button to close the application.

## NLP Model for Task Categorization
- The model is trained using the task_data.csv file, which contains sample tasks and their categories.
- The user_input_processing.py file contains the code for training the model and making predictions.
- The model uses TF-IDF vectorization and a Support Vector Machine (SVM) classifier for categorization.
- Grid search cross-validation is used to find optimal parameters for the model.

**Users can customize categorization by modifying the task_data.csv file. To add or remove data**
 1. Open the task_data.csv file.
 2. Add new rows with tasks and their corresponding categories or remove existing rows.
 3. Save the file.
 4. Run the build_csv.py script to regenerate the CSV file used by the model:
 
```bash
python build_csv.py
```
 5. Restart the application for changes to take effect. 


