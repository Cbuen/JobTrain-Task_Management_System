import sys
import json
import os
import requests
from datetime import datetime

# Importing PyQt5 modules for GUI components
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget
from PyQt5.QtCore import QTimer, Qt

# links this file to my language processing model
from user_input_processesing import predict_category


# Main window class for the Task Management System
class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Management System")
        self.setGeometry(100, 100, 800, 600)

        self.task_list = []

        self.organized_tasks = dict()
        
        # Timeapi to have a live clock
        self.DEFAULT_TIMEZONE = "zone?timeZone=America/Los_Angeles"
        self.api_url = "https://timeapi.io/api/Time/current/{}".format(self.DEFAULT_TIMEZONE)

        # Initialize current_date and current_time
        self.current_date = ""
        self.current_time = ""

        # call to the time api before setup UI is created
        self.fetch_time()

        self.setup_ui()
        self.start_clock()

    # Fetch the current time before setting up the UI
    def fetch_time(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()
                
                self.current_date = data.get("date")
                self.current_time = data.get('time')
                self.current_time = self.convert_to_regular_time(self.current_time)
                return self.current_time

        except Exception as e:
            print(e)

    # Function to set up the user interface

    def setup_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Add a welcome lABEL
        label = QLabel("Welcome to the task management system")

        # Add labels to show the current date and time
        self.date_label = QLabel(self.current_date)
        main_layout.addWidget(self.date_label)

        self.time_label = QLabel(self.current_time)
        main_layout.addWidget(self.time_label)


          # Add buttons for various actions
        add_button = QPushButton("Add New Task")
        add_button.clicked.connect(self.add_task)

        view_button = QPushButton("View Tasks")
        view_button.clicked.connect(self.view_tasks)

        organized_task_buttton = QPushButton("Organized Task View")
        organized_task_buttton.clicked.connect(self.view_task_categories)

        # Added button to generate users task categories
        generate_task_categories_button = QPushButton("Generate your task categories")

        # Connects button to the self.generate_categories merthod
        generate_task_categories_button.clicked.connect(self.generate_categories)

        complete_button = QPushButton("Complete Task")
        complete_button.clicked.connect(self.complete_task)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

    
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        save_button.setGeometry(100, 100, 50, 40)

        clean_save_button = QPushButton("Clean Save")
        clean_save_button.clicked.connect(self.clean_save)

        main_layout.addWidget(label)
        main_layout.addWidget(save_button)
        main_layout.addWidget(clean_save_button)
        main_layout.addWidget(add_button)   
        main_layout.addWidget(view_button)
        main_layout.addWidget(organized_task_buttton)
        main_layout.addWidget(generate_task_categories_button)
        main_layout.addWidget(complete_button)
        main_layout.addWidget(exit_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_task(self):
        add_dialog = AddTaskDialog(self)
        if add_dialog.exec_() == QDialog.Accepted:
            task = add_dialog.task_edit.text()
            self.task_list.append(task)

    def view_tasks(self):
        view_dialog = ViewTasksDialog(self, self.task_list)
        view_dialog.exec_()

    def view_task_categories(self):
        view_categories = ViewOrganizedTasks(self, self.organized_tasks)
        view_categories.exec_()


    def generate_categories(self):
        if self.task_list:
            temp_list = predict_category(self.task_list)

            for i in range(len(temp_list)):
                category = str(temp_list[i])
                task = self.task_list[i]

                if category not in self.organized_tasks:
                    self.organized_tasks[category] = []

                if task not in self.organized_tasks[category]:
                    self.organized_tasks[category].append(task)
        else:
            self.task_list.clear()



    def complete_task(self):
        complete_dialog = CompleteTaskDialog(self, self.task_list)
        if complete_dialog.exec_() == QDialog.Accepted:
            completed_task = complete_dialog.task_list.currentRow()

            self.remove_from_ogranized_task(completed_task)
            # self.task_list.pop(completed_task)

    def closeEvent(self, event):
        reply = ConfirmDialog.confirm_exit(self)
        if reply == ConfirmDialog.Yes:
            event.accept()
        else:
            event.ignore()

    def convert_to_regular_time(self, time_string):
        time_obj = datetime.strptime(time_string, "%H:%M")

        return time_obj.strftime("%I:%M %p")


    def update_time(self):
        current_time = self.fetch_time()
        self.time_label.setText(current_time)

    def start_clock(self):
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)

    def remove_from_ogranized_task(self, task_to_remove):
        target_task = self.task_list[task_to_remove]

        for key in list(self.organized_tasks.keys()):
            if target_task in self.organized_tasks[key]:
                if len(self.organized_tasks[key]) == 1:
                    del self.organized_tasks[key]
                else:
                    self.organized_tasks[key].remove(target_task)
        self.task_list.pop(task_to_remove)

    def save(self):
        filename = 'current_tasks.json'
        existing_tasks = {}
        
        # Check if the file exists and read existing tasks
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    existing_tasks = json.load(file)
                except json.JSONDecodeError:
                    # If the file is empty or invalid JSON, we'll start with an empty dict
                    pass
        
        # Merge existing tasks with current tasks
        for category, tasks in self.organized_tasks.items():
            if category in existing_tasks:
                existing_tasks[category].extend(task for task in tasks if task not in existing_tasks[category])
            else:
                existing_tasks[category] = tasks
        
        # Save the merged tasks
        with open(filename, 'w') as file:
            json.dump(existing_tasks, file, indent=4)
    
    def clean_save(self):
        filename = 'current_tasks.json'
        
        # Save only the current tasks, overwriting any existing data
        with open(filename, 'w') as file:
            json.dump(self.organized_tasks, file, indent=4)
    




class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")

        layout = QVBoxLayout()

        self.task_edit = QLineEdit()

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.accept)

        layout.addWidget(self.task_edit)
        layout.addWidget(add_button)

        self.setLayout(layout)


class ViewTasksDialog(QDialog):
    def __init__(self, parent=None, tasks=[]):
        super().__init__(parent)
        self.setWindowTitle("View Tasks")

        layout = QVBoxLayout()

        self.task_list = QTextEdit()
        self.task_list.setReadOnly(True)
        self.task_list.setPlainText("\n".join(tasks))

        layout.addWidget(self.task_list)

        self.setLayout(layout)

class ViewOrganizedTasks(QDialog):
    def __init__(self, parent=None, organized_tasks={}):
        super().__init__(parent)
        self.setWindowTitle("Grouped Tasks")
        self.organized_tasks = organized_tasks

        layout = QHBoxLayout()

        # Category list
        self.category_list = QListWidget()
        self.category_list.addItems(self.organized_tasks.keys())
        self.category_list.itemClicked.connect(self.show_category_tasks)
        layout.addWidget(self.category_list)

        # Tasks for selected category
        self.category_tasks = QListWidget()
        layout.addWidget(self.category_tasks)

        self.setLayout(layout)

    def show_category_tasks(self, item):
        category = item.text()
        tasks = self.organized_tasks.get(category, [])
        self.category_tasks.clear()
        self.category_tasks.addItems(tasks)

class CompleteTaskDialog(QDialog):
    def __init__(self, parent=None, tasks=[]):
        super().__init__(parent)
        self.setWindowTitle("Complete Task")

        layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.task_list.addItems(tasks)

        complete_button = QPushButton("Complete")
        complete_button.clicked.connect(self.accept)

        layout.addWidget(self.task_list)
        layout.addWidget(complete_button)

        self.setLayout(layout)



class ConfirmDialog(QDialog):
    Yes = QDialog.Accepted
    No = QDialog.Rejected

    @staticmethod
    def confirm_exit(parent=None):
        dialog = ConfirmDialog(parent)
        result = dialog.exec_()
        if result == ConfirmDialog.Yes:
            return ConfirmDialog.Yes
        else:
            return ConfirmDialog.No

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Exit")

        layout = QVBoxLayout()

        label = QLabel("Are you sure you want to exit?")

        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton("No")
        no_button.clicked.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(yes_button)
        layout.addWidget(no_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # setting a global style sheet
    app.setStyleSheet("""                      
        * {
            font-family: "Arial";
            font-size: 14px;
            border-radius: 8px;
        }              
        QPushButton {
            background-color: #007ACC;
            color: white;
            font-size: 14px;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #005A9E;
        }
        QPushButton:pressed {
            background-color: #004275;
        }
    """)


    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec_())
