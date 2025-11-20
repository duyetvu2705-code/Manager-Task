## =======================================================================
## ||                     TASKS MANAGE                                  ||
## =======================================================================


        ##HELP YOU MANAGA ALL THE PROJECT OF YOUR COMPANY
        ##EASY TO FIX AND EDIT
        ##FOLLOW THE PERPENT OF STATUS PROGRESS OF PROJECTS, TASKS, ITEMS.


##*********************************
##* Import library Modules        *
##********************************* 
import os
from datetime import datetime, date
import re

##*********************************
##*          Help function        *
##********************************* 

def check_y_or_n(choice):
    while True:
        if choice.lower() in ['y', 'n']:
            return choice.lower()
        choice = input('!!! Wrong input!!! Enter y or n: ').lower()

def validate_date(date_str):
    """Validate date format MM/DD/YYYY and ensure it's a valid date."""
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def calculate_days_left(due_date_str):
    """Calculate days left from today to due date."""
    try:
        due_date = datetime.strptime(due_date_str, '%m/%d/%Y').date()
        today = date.today()
        delta = due_date - today
        return delta.days
    except ValueError:
        return None

##*********************************
##* 1         Add Data            *
##*********************************  

def main_input(): 
    while True:
        project_name = input('Name of new project: ')
        project_status = 0.0
        project_desc = input("Write a description: (Enter to skip): ")
        while True:
            due_date = input("Enter due date (MM/DD/YYYY): ")
            if validate_date(due_date):
                break
            print("Invalid date format. Please use MM/DD/YYYY.")
        test = any(project["name"] == project_name for project in projects)
        if test:
            choice_project = input('!!! Project exists !!! [?]Would you like to retry(r) or continue(c): ').lower()
            if choice_project == 'c':
                break
            else:
                continue
        else:
            add_project(project_name, project_status, project_desc, due_date)
        break
    task_num = 1    
    while True:
        choice_task = input(f"[?] Would you like to add ''Task'' for project {project_name} (y/n): ").lower()
        task_status = 0.0
        choice = check_y_or_n(choice_task)
        if choice == 'y':
            print()
            task_name = input(f'\t<{task_num}> Name of task: ')
            add_task(project_name, task_name, task_status)
            add_item_input = input(f"\t\n[?] Would you like add ''Item'' for Task '{task_name}'? (y/n): ").lower()
            add_item_input = check_y_or_n(add_item_input)
            item_num = 1               
            if add_item_input == 'y':
                while True:
                    print()
                    item_name = input(f"\t\t<{item_num}> Name of Item: ")
                    in_status = input(f"\t\tInput Item status ('y':[Completed] / 'n':[Incompleted] ) ")
                    item_num += 1
                    in_status = check_y_or_n(in_status)
                    status = True if in_status == 'y' else False
                    add_item(project_name, task_name, item_name, status)     
                    more_items = input("\t\t[?] Would you like to add more Item? (y/n): ").lower()
                    print()
                    more_items = check_y_or_n(more_items)
                    if more_items != 'y':
                        break
            task_num += 1
        else:
            menu()
            break

def add_project(name, project_status, description, due_date):
    project = {
        "name": name,
        "tasks": [],
        "description": description,
        "status": project_status,
        "due_date": due_date
    }
    projects.append(project)
    print(f"->Project '{name}' is added with due date {due_date}.")
    print()
def add_task(project_name, task_name, task_status):
    for project in projects:
        if project["name"] == project_name:
            task = {
                "name": task_name,
                "items": [],
                "status": task_status
            }
            project["tasks"].append(task)
            print(f"\t->Task '{task_name}' is added to '{project_name}'.")
            return True        
    print(f"Can not find '{project_name}'.")
    return False

def add_item(project_name, task_name, item_name, status):
    for project in projects:
        if project["name"] == project_name:
            for task in project["tasks"]:
                if task["name"] == task_name:
                    item = {
                        "name": item_name,
                        "status": status,
                        "sub_items": []
                    }
                    task["items"].append(item)
                    print(f"\t\t->Item '{item_name}' is added to '{task_name}'.")
                    return True
            print(f"Can not find '{task_name}'.")
            return False
    print(f"Can not find '{project_name}'.")
    return False

##*********************************
##* 2      Show Data Menu         *
##*********************************           

def show_data():
    while True:
        print()
        print('     ----<<<>>>-----   ')
        print(' <2>   Show Data ')
        print('     ----<<<>>>-----   ')
        print('    [a] Show Projects')
        print('    [b] Show Tasks')
        print('    [c] Show Items' )
        print('    [d] Show all data')
        print('    [e] Back ')
        print('     ----<<<>>>-----   ')
        letter = input('    >>> Choose the next option in [Show Data]: ')
        print()
        if letter == 'a':
            show_project()
        elif letter == 'b':
            show_project()
            project_num = int(input('>>> Choose the number of project to show: '))
            show_tasks(project_num)
        elif letter == 'c':
            show_project()
            project_num = int(input('>>> Choose the number of project to show: '))
            show_tasks(project_num)
            task_num = int(input('\t>>> Choose the number of task to show: '))
            show_items(project_num, task_num)                   
        elif letter == 'd':
            show_all_data()        
        elif letter == 'e':
            menu()
            break
        else: 
            print('Not a valid input. Try again: ')

def show_project():
    update_completion_status()
    if not projects:
        print("There are no projects")
        return
    print(' Project list: ')  
    i = 1
    for project in projects:
        status = f"{project['status']:.2%}" if isinstance(project['status'], float) else "0.00%"
        description = '[None]' if project["description"] == '' else project["description"]
        due_date = project["due_date"]
        days_left = calculate_days_left(due_date)
        days_left_str = f"{days_left} days left" if days_left is not None else "Invalid date"
        print(f"<{i}> {project['name']}")
        print(f" \tDescription: {description}")
        print(f" \tProgress Status: {status}")
        print(f" \tDue Date: {due_date} ({days_left_str})")
        i += 1
        
def show_tasks(project_num):
    update_completion_status()
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return []
    project = projects[project_num - 1]
    project_name = project["name"]
    if not project["tasks"]:
        print("No Task in the Project")
        return []
    status = f"{project['status']:.2%}" if isinstance(project['status'], float) else "0.00%"
    print(f"\nList tasks of project  --- <{project_num}> --- ")
    i = 1
    for task in project["tasks"]:
        status = f"{task['status']:.2%}" if isinstance(task['status'], float) else "0.00%"
        print(f"\t>{i}. {task['name']:<40}{'status: ':>10}{status}")
        i += 1
    return [task["name"] for task in project["tasks"]]

def show_items(project_num, task_num):
    update_completion_status()
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    if not task["items"]:
        print(f'\t\tItem: No Item')
    else:
        i = 1
        for item in task["items"]:
            comp_status = 'Completed' if item["status"] else 'Incompleted'
            print(f"\t\t<{i}> Item: {item['name']:<40}{'status: ':>10}[{comp_status}]")
            i += 1

def show_all_data():
    update_completion_status()
    if not projects:
        print("No projects in Task")
        return
    project_num = 1
    for project in projects:
        status = f"{project['status']:.2%}" if isinstance(project['status'], float) else "0.00%"
        due_date = project["due_date"]
        days_left = calculate_days_left(due_date)
        days_left_str = f"{days_left} days left" if days_left is not None else "Invalid date"
        print(f"\n<{project_num}>. Project: {project['name']:<40}{'Main progress: ':>10}{status}")
        print(f"Due Date: {due_date} ({days_left_str})")
        project_num += 1
        task_num = 1
        for task in project["tasks"]:
            status = f"{task['status']:.2%}" if isinstance(task['status'], float) else "0.00%"
            print(f"  \t>{task_num}. Task: {task['name']:<40}{'Progress: ':>10}{status}")
            task_num += 1
            if not task["items"]:
                print(f'\t\tItem: No Item')
            else:
                item_num = 1
                for item in task["items"]:
                    comp_status = 'Completed' if item["status"] else 'Incompleted'
                    print(f"\t\t[{item_num}]. Item: {item['name']:<40}{'':>10}[{comp_status}]")
                    item_num += 1

##*********************************
##* 3      Mark Complete          *
##*********************************

def update_completion_status():
    for project in projects:
        total_task_status = 0
        num_tasks = len(project["tasks"])
        for task in project["tasks"]:
            items_status = 0
            num_items = len(task["items"])
            if num_items != 0:
                for item in task["items"]:
                    items_status += 1 if item["status"] else 0
                task_status = items_status / num_items
                task["status"] = task_status
                total_task_status += task_status
            else:
                task["status"] = 0.0 
        if num_tasks != 0:
            project_status = total_task_status / num_tasks
            project["status"] = project_status
        else:
            project["status"] = 0.0 

def mark_completion():
    while True:
        print()
        print('     ----<<<>>>-----   ')
        print('<3> Mark Completion')
        print('     ----<<<>>>-----   ')
        print('    [a] Mark Project Complete')
        print('    [b] Mark Task Complete')
        print('    [c] Mark Item Complete')
        print('    [d] Back')
        print('     ----<<<>>>-----   ')
        letter = input('    >>> Choose an option: ').lower()
        print()
        if letter == 'a':
            if not projects:  
                print("No projects available to mark.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                mark_project_complete(project_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'b':
            if not projects: 
                print("No projects available to mark tasks.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]: 
                    print("No tasks available to mark in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                mark_task_complete(project_num, task_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'c':
            if not projects:  
                print("No projects available to mark items.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]:  
                    print("No tasks available in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                if not (1 <= task_num <= len(projects[project_num - 1]["tasks"])):
                    print("Invalid task number.")
                    continue
                if not projects[project_num - 1]["tasks"][task_num - 1]["items"]:  
                    print("No items available to mark in this task.")
                    continue
                show_items(project_num, task_num)
                print()
                item_num = int(input('\t\t>>> Item number: '))
                mark_item_complete(project_num, task_num, item_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'd':
            menu()
            break
        else:
            print("Invalid option. Try again.")

def mark_item_complete(project_num, task_num, item_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    if not (1 <= item_num <= len(task["items"])):
        print("Invalid item number.")
        return
    item = task["items"][item_num - 1]
    item["status"] = not item["status"]
    print(f"Item '{item['name']}' marked as {'Completed' if item['status'] else 'Incompleted'}.")
    update_completion_status()

def mark_task_complete(project_num, task_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    task["status"] = 1.0 if task["status"] != 1.0 else 0.0
    for item in task["items"]:
        item["status"] = True if task["status"] == 1.0 else False
    print(f"Task '{task['name']}' marked as {'Completed' if task["status"] == 1.0 else 'Incompleted'}.")
    update_completion_status()

def mark_project_complete(project_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    project["status"] = 1.0 if project["status"] != 1.0 else 0.0
    for task in project["tasks"]:
        task["status"] = project["status"]
        for item in task["items"]:
            item["status"] = True if project["status"] == 1.0 else False
    print(f"Project '{project['name']}' marked as {'Completed' if project["status"] == 1.0 else 'Incompleted'}.")
    update_completion_status()

##*********************************
##* 4      Edit Data Menu         *
##*********************************        
def edit_data():
    while True:
        print()
        print('     ----<<<>>>-----   ')
        print('<4> Edit Data')
        print('     ----<<<>>>-----   ')
        print('     [a] Edit Project')
        print('     [b] Edit Task')
        print('     [c] Edit Item')
        print('     [d] Back')
        print('     ----<<<>>>-----   ')
        letter = input('    >>> Choose an option: ').lower()
        print()
        if letter == 'a':
            if not projects:  
                print("No projects available to edit.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                edit_project(project_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'b':
            if not projects:
                print("No projects available to edit tasks.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]:  
                    print("No tasks available to edit in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                edit_task(project_num, task_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'c':
            if not projects:  
                print("No projects available to edit items.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]:  
                    print("No tasks available in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                if not (1 <= task_num <= len(projects[project_num - 1]["tasks"])):
                    print("Invalid task number.")
                    continue
                if not projects[project_num - 1]["tasks"][task_num - 1]["items"]:  
                    print("No items available to edit in this task.")
                    continue
                show_items(project_num, task_num)
                print()
                item_num = int(input('\t\t>>> Item number: '))
                edit_item(project_num, task_num, item_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'd':
            menu()
            break
        else:
            print("Invalid option. Try again.")

def edit_project(project_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    print(f"Editing project: {project['name']}")
    new_name = input("Enter new project name (leave blank to keep unchanged): ")
    if new_name:
        project["name"] = new_name
        print(f"Project name updated to '{new_name}'.")
    new_due_date = input("Enter new due date (MM/DD/YYYY, leave blank to keep unchanged): ")
    if new_due_date and validate_date(new_due_date):
        project["due_date"] = new_due_date
        print(f"Due date updated to '{new_due_date}'.")
    status_input = input("Mark project as completed? (y/n): ")
    status_input = check_y_or_n(status_input)
    if status_input == 'y':
        project["status"] = 1.0
        for task in project["tasks"]:
            task["status"] = 1.0
            for item in task["items"]:
                item["status"] = True
        print("Project and all tasks/items marked as completed.")

        
    task_num = 1
    project_name = project["name"]
    while True:
        choice_task = input(f"[?] Would you like to add ''Task'' for project {project_name} (y/n): ").lower()
        task_status = 0.0
        choice = check_y_or_n(choice_task)
        if choice == 'y':
            print()
            task_name = input(f'\t<{task_num}> Name of task: ')
            add_task(project_name, task_name, task_status)
            add_item_input = input(f"\t\n[?] Would you like add ''Item'' for Task '{task_name}'? (y/n): ").lower()
            add_item_input = check_y_or_n(add_item_input)
            item_num = 1               
            if add_item_input == 'y':
                while True:
                    print()
                    item_name = input(f"\t\t<{item_num}> Name of Item: ")
                    in_status = input(f"\t\tInput Item status ('y':[Completed] / 'n':[Incompleted] ) ")
                    item_num += 1
                    in_status = check_y_or_n(in_status)
                    status = True if in_status == 'y' else False
                    add_item(new_name, task_name, item_name, status)     
                    more_items = input("\t\t[?] Would you like to add more Item? (y/n): ").lower()
                    print()
                    more_items = check_y_or_n(more_items)
                    if more_items != 'y':
                        break
            task_num += 1
        else:
            break    
    update_completion_status()

def edit_task(project_num, task_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    print(f"Editing task: {task['name']} in project: {project['name']}")
    new_name = input("Enter new task name (leave blank to keep unchanged): ")
    if new_name:
        task["name"] = new_name
        print(f"Task name updated to '{new_name}'.")
    status_input = input("Mark task as completed? (y/n): ")
    status_input = check_y_or_n(status_input)
    if status_input == 'y':
        task["status"] = 1.0
        for item in task["items"]:
            item["status"] = True
        print("Task and all items marked as completed.")
        
    project_name =  project["name"]   
    task_name = task["name"]    
    add_item_input = input(f"\t\n[?] Would you like add ''Item'' for Task '{task_name}'? (y/n): ").lower()
    add_item_input = check_y_or_n(add_item_input)
    item_num = 1
    if add_item_input == 'y':
        while True:
            print()
            item_name = input(f"\t\t<{item_num}> Name of Item: ")
            in_status = input(f"\t\tInput Item status ('y':[Completed] / 'n':[Incompleted] ) ")
            item_num += 1
            in_status = check_y_or_n(in_status)
            status = True if in_status == 'y' else False
            add_item(project_name, task_name, item_name, status)     
            more_items = input("\t\t[?] Would you like to add more Item? (y/n): ").lower()
            print()
            more_items = check_y_or_n(more_items)
            if more_items != 'y':
                break
            
    update_completion_status()

def edit_item(project_num, task_num, item_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    if not (1 <= item_num <= len(task["items"])):
        print("Invalid item number.")
        return
    item = task["items"][item_num - 1]
    print(f"Editing item: {item['name']} in task: {task['name']}")
    new_name = input("Enter new item name (leave blank to keep unchanged): ")
    if new_name:
        item["name"] = new_name
        print(f"Item name updated to '{new_name}'.")
    status_input = input("Mark item as completed? (y/n): ")
    status_input = check_y_or_n(status_input)
    item["status"] = True if status_input == 'y' else False
    print(f"Item status updated to {'Completed' if item['status'] else 'Incompleted'}.")
    update_completion_status()

##*********************************
##* 5      Delete Data Menu       *
##*********************************       

def delete_data():
    while True:
        print()
        print('     ----<<<>>>-----   ')
        print('<5> Delete Data')
        print('     ----<<<>>>-----   ')
        print('    [a] Delete Project')
        print('    [b] Delete Task')
        print('    [c] Delete Item')
        print('    [d] Back')
        print('     ----<<<>>>-----   ')
        letter = input('    >>> Choose an option: ').lower()
        print()
        if letter == 'a':
            if not projects:  
                print("No projects available to delete.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                delete_project(project_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'b':
            if not projects: 
                print("No projects available to delete tasks.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]:  
                    print("No tasks available to delete in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                delete_task(project_num, task_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'c':
            if not projects:  # Kiểm tra nếu không có project
                print("No projects available to delete items.")
                continue
            show_project()
            print()
            try:
                project_num = int(input('>>> Project number: '))
                if not (1 <= project_num <= len(projects)):
                    print("Invalid project number.")
                    continue
                if not projects[project_num - 1]["tasks"]: 
                    print("No tasks available in this project.")
                    continue
                show_tasks(project_num)
                print()
                task_num = int(input('\t>>> Task number: '))
                if not (1 <= task_num <= len(projects[project_num - 1]["tasks"])):
                    print("Invalid task number.")
                    continue
                if not projects[project_num - 1]["tasks"][task_num - 1]["items"]:  
                    print("No items available to delete in this task.")
                    continue
                show_items(project_num, task_num)
                print()
                item_num = int(input('\t\t>>> Item number: '))
                delete_item(project_num, task_num, item_num)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif letter == 'd':
            menu()
            break
        else:
            print("Invalid option. Try again.")

def delete_project(project_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects.pop(project_num - 1)
    print(f"Project '{project['name']}' has been deleted.")

def delete_task(project_num, task_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"].pop(task_num - 1)
    print(f"Task '{task['name']}' has been deleted from '{project['name']}'.")
    update_completion_status()

def delete_item(project_num, task_num, item_num):
    if not (1 <= project_num <= len(projects)):
        print("Invalid project number.")
        return
    project = projects[project_num - 1]
    if not (1 <= task_num <= len(project["tasks"])):
        print("Invalid task number.")
        return
    task = project["tasks"][task_num - 1]
    if not (1 <= item_num <= len(task["items"])):
        print("Invalid item number.")
        return
    item = task["items"].pop(item_num - 1)
    print(f"Item '{item['name']}' has been deleted from '{task['name']}'.")
    update_completion_status()

##*********************************
##* 6      Save to File           *
##*********************************

def save_to_txt():
    update_completion_status()
    filename = input("Enter the filename to save (e.g., projects.txt): ") + '.txt'
    try:
        file = open(filename, 'w', encoding='utf-8')
        file.write("Project Management Data\n")
        file.write("======================\n\n")
        if not projects:
            file.write("No projects available.\n")
            print("No projects to save.")
            return
        for project in projects:
            status = f"{project['status']:.2%}" if isinstance(project['status'], float) else "0.00%"
            description = '[None]' if project["description"] == '' else project["description"]
            due_date = project["due_date"]
            days_left = calculate_days_left(due_date)
            days_left_str = f"{days_left} days left" if days_left is not None else "Invalid date"
            file.write(f"Project: {project['name']}\n")
            file.write(f"Description: {description}\n")
            file.write(f"Progress Status: {status}\n")
            file.write(f"Due Date: {due_date} ({days_left_str})\n")
            file.write(f"\n")
            if not project["tasks"]:
                file.write("  No tasks.\n")
            else:
                for task in project["tasks"]:
                    task_status = f"{task['status']:.2%}" if isinstance(task['status'], float) else "0.00%"
                    file.write(f"  Task: {task['name']:<40} (Status: {task_status:>10})\n")
                    if not task["items"]:
                        file.write("    No items.\n")
                    else:
                        for item in task["items"]:
                            item_status = 'Completed' if item["status"] else 'Incompleted'
                            file.write(f"    Item: {item['name']} (Status: {item_status})\n")
                file.write("\n")
        print(f"Data successfully saved to '{filename}'.txt")
        print(f"Current working directory: {os.getcwd()}")
    except Exception as e:
        print(f"Error saving file: {e}")

##*********************************
##*          Main Menu            *
##*********************************

def menu():
    print()
    print('   ------<MENU>------    ')                          
    print(' <1>   Create New Project')                      
    print(' <2>   Show data        ')
    print(' <3>   Complete Mark    ')
    print(' <4>   Edit data        ')
    print(' <5>   Delete           ')
    print(' <6>   Save to .txt')
    print(' <7>   Exit             ')
    print('   ------<<<>>>-------')

def main():
    menu()
    while True:
        num = input('Choose a number(1-7) in menu: ')
        print()
        if num == "1":
            main_input()
        elif num == "2":
            show_data()
        elif num == "3":
            mark_completion()
        elif num == "4":
            edit_data()
        elif num == "5":
            delete_data()
        elif num == "6":
            save_to_txt()
        elif num == "7":
            print(' Exiting the program. See you! ')
            os._exit(0)
        else: 
            print(' Not a valid number. Try a number (1-7): ')



##*********************************
##*      Run program             *
##*********************************
projects = []
if __name__ == "__main__":
    main()
