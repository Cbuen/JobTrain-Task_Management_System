task = []


def add_task():
    user_task = input("Enter Your Task")
    task.append(user_task)


def view_task():
    for i, j in enumerate(task):
        print(i + 1, " ", j)


def complete_task():
    task_num = int(input("Enter task that you have completed"))
    task.pop(task_num - 1)
    view_task()


def show_menu():
    print("Welcome to task management system")
    print("1. Add new task")
    print("2. view task")
    print("3. complete task")
    print("4. Exit")


def todo_app():
    show_menu()
    while True:
        choice = int(input("Enter Your Choice "))

        if choice == 1:
            add_task()
        elif choice == 2:
            view_task()
        elif choice == 3:
            complete_task()
        elif choice == 4:
            break
        else:
            print("Invalid Input")


todo_app()