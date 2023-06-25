import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Management System")
        self.setGeometry(100, 100, 400, 300)

        self.task_list = []

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        label = QLabel("Welcome to the task management system")

        add_button = QPushButton("Add New Task")
        add_button.clicked.connect(self.add_task)

        view_button = QPushButton("View Tasks")
        view_button.clicked.connect(self.view_tasks)

        complete_button = QPushButton("Complete Task")
        complete_button.clicked.connect(self.complete_task)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

        main_layout.addWidget(label)
        main_layout.addWidget(add_button)
        main_layout.addWidget(view_button)
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

    def complete_task(self):
        complete_dialog = CompleteTaskDialog(self, self.task_list)
        if complete_dialog.exec_() == QDialog.Accepted:
            completed_task = complete_dialog.task_list.currentRow()
            self.task_list.pop(completed_task)

    def closeEvent(self, event):
        reply = ConfirmDialog.confirm_exit(self)
        if reply == ConfirmDialog.Yes:
            event.accept()
        else:
            event.ignore()


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
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec_())
