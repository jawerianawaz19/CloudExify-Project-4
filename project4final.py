# PYTHON To Do List
# CloudExify Python Internship - Month 2 Project 4(final version)
# Jaweria Nawaz | Registration No: CX-INT-2026-PY-0119


import json
import os
from datetime import datetime, date

FILE = "tasks.json"
next_id = 1

def load_tasks():
    global next_id
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        tasks = json.load(f)
    if tasks:
        next_id = max(t["id"] for t in tasks) + 1
    return tasks

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    global next_id
    print("\n--- ADD NEW TASK ---")
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty!")
        return
    print("Priority: 1) High  2) Medium  3) Low")
    while True:
        choice = input("Select (1-3): ").strip()
        if choice == "1":
            priority = "High"
            break
        elif choice == "2":
            priority = "Medium"
            break
        elif choice == "3":
            priority = "Low"
            break
        else:
            print("Enter 1, 2, or 3!")
    print("Category: 1) Work  2) Study  3) Personal")
    while True:
        choice = input("Select (1-3): ").strip()
        if choice == "1":
            category = "Work"
            break
        elif choice == "2":
            category = "Study"
            break
        elif choice == "3":
            category = "Personal"
            break
        else:
            print("Enter 1, 2, or 3!")
    due_date = input("Due date (YYYY-MM-DD) or skip: ").strip()
    if not due_date:
        due_date = "No due date"
    task = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "status": "Pending",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    next_id += 1
    save_tasks(tasks)
    print(f"Task added! ID: {task['id']}")

def view_tasks(tasks, filter_status=None, filter_priority=None, filter_category=None):
    display = tasks
    if filter_status:
        display = [t for t in display if t["status"] == filter_status]
    if filter_priority:
        display = [t for t in display if t["priority"] == filter_priority]
    if filter_category:
        display = [t for t in display if t.get("category") == filter_category]
    if not display:
        print("\nNo tasks found!")
        return
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    display = sorted(display, key=lambda t: priority_order.get(t["priority"], 4))
    print(f"\n{'ID':<5} {'Title':<25} {'Priority':<10} {'Category':<12} {'Status':<10} {'Due Date'}")
    print("-" * 85)
    for t in display:
        status_mark = "DONE" if t["status"] == "Done" else "..."
        category = t.get("category", "N/A")
        print(f"{t['id']:<5} {t['title']:<25} {t['priority']:<10} {category:<12} {status_mark:<10} {t['due_date']}")

def mark_done(tasks):
    view_tasks(tasks, filter_status="Pending")
    try:
        task_id = int(input("\nEnter task ID to mark done: "))
    except ValueError:
        print("Please enter a number!")
        return
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Done":
                print("Task is already done!")
            else:
                task["status"] = "Done"
                save_tasks(tasks)
                print(f"Task '{task['title']}' marked as done!")
            return
    print(f"No task found with ID {task_id}")

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print("Please enter a number!")
        return
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            confirm = input(f"Delete '{task['title']}'? (yes/no): ").lower()
            if confirm in ["yes", "y"]:
                tasks.pop(i)
                save_tasks(tasks)
                print("Task deleted!")
            return
    print(f"No task found with ID {task_id}")

def show_stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "Done")
    pending = total - done
    high = sum(1 for t in tasks if t["priority"] == "High" and t["status"] == "Pending")
    print("\n=== TASK STATISTICS ===")
    print(f"Total Tasks   : {total}")
    print(f"Completed     : {done}")
    print(f"Pending       : {pending}")
    print(f"High Priority : {high} pending")
    if total > 0:
        pct = (done / total) * 100
        print(f"Completion    : {pct:.0f}%")

def show_overdue(tasks):
    today = date.today()
    overdue = []
    for t in tasks:
        if t["status"] == "Done":
            continue
        due = t["due_date"]
        if due == "No due date":
            continue
        try:
            due_dt = datetime.strptime(due, "%Y-%m-%d").date()
            if due_dt < today:
                overdue.append(t)
        except ValueError:
            continue
    if not overdue:
        print("\nNo overdue tasks!")
        return
    view_tasks(overdue)

def show_due_today(tasks):
    today_str = date.today().strftime("%Y-%m-%d")
    due_today = [t for t in tasks if t["due_date"] == today_str and t["status"] != "Done"]
    if not due_today:
        print("\nNo tasks due today!")
        return
    view_tasks(due_today)

def search_tasks(tasks):
    keyword = input("\nEnter keyword to search in title: ").strip().lower()
    if not keyword:
        print("Keyword cannot be empty!")
        return
    results = [t for t in tasks if keyword in t["title"].lower()]
    if not results:
        print("\nNo matching tasks found!")
        return
    view_tasks(results)

def edit_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("\nEnter task ID to edit: "))
    except ValueError:
        print("Please enter a number!")
        return
    for task in tasks:
        if task["id"] == task_id:
            print(f"\nEditing: {task['title']}")
            print("1) Edit title")
            print("2) Edit priority")
            print("3) Edit both")
            choice = input("Select (1-3): ").strip()
            if choice in ["1", "3"]:
                new_title = input("New title: ").strip()
                if new_title:
                    task["title"] = new_title
                else:
                    print("Title left unchanged.")
            if choice in ["2", "3"]:
                print("Priority: 1) High  2) Medium  3) Low")
                while True:
                    p_choice = input("Select (1-3): ").strip()
                    if p_choice == "1":
                        task["priority"] = "High"
                        break
                    elif p_choice == "2":
                        task["priority"] = "Medium"
                        break
                    elif p_choice == "3":
                        task["priority"] = "Low"
                        break
                    else:
                        print("Enter 1, 2, or 3!")
            save_tasks(tasks)
            print("Task updated!")
            return
    print(f"No task found with ID {task_id}")

def main():
    tasks = load_tasks()
    print(f"Loaded {len(tasks)} tasks.")
    while True:
        print("\n=== TO-DO LIST MANAGER ===")
        print("1. Add task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View high priority")
        print("5. Mark task as done")
        print("6. Delete task")
        print("7. Show statistics")
        print("8. Show overdue tasks")
        print("9. Show tasks due today")
        print("10. Search tasks by keyword")
        print("11. Edit task")
        print("12. Exit")
        choice = input("Choose (1-12): ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, filter_status="Pending")
        elif choice == "4":
            view_tasks(tasks, filter_priority="High")
        elif choice == "5":
            mark_done(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            show_stats(tasks)
        elif choice == "8":
            show_overdue(tasks)
        elif choice == "9":
            show_due_today(tasks)
        elif choice == "10":
            search_tasks(tasks)
        elif choice == "11":
            edit_task(tasks)
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main();import json
import os
from datetime import datetime, date

FILE = "tasks.json"
next_id = 1

def load_tasks():
    global next_id
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        tasks = json.load(f)
    if tasks:
        next_id = max(t["id"] for t in tasks) + 1
    return tasks

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    global next_id
    print("\n--- ADD NEW TASK ---")
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty!")
        return
    print("Priority: 1) High  2) Medium  3) Low")
    while True:
        choice = input("Select (1-3): ").strip()
        if choice == "1":
            priority = "High"
            break
        elif choice == "2":
            priority = "Medium"
            break
        elif choice == "3":
            priority = "Low"
            break
        else:
            print("Enter 1, 2, or 3!")
    print("Category: 1) Work  2) Study  3) Personal")
    while True:
        choice = input("Select (1-3): ").strip()
        if choice == "1":
            category = "Work"
            break
        elif choice == "2":
            category = "Study"
            break
        elif choice == "3":
            category = "Personal"
            break
        else:
            print("Enter 1, 2, or 3!")
    due_date = input("Due date (YYYY-MM-DD) or skip: ").strip()
    if not due_date:
        due_date = "No due date"
    task = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "status": "Pending",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    next_id += 1
    save_tasks(tasks)
    print(f"Task added! ID: {task['id']}")

def view_tasks(tasks, filter_status=None, filter_priority=None, filter_category=None):
    display = tasks
    if filter_status:
        display = [t for t in display if t["status"] == filter_status]
    if filter_priority:
        display = [t for t in display if t["priority"] == filter_priority]
    if filter_category:
        display = [t for t in display if t.get("category") == filter_category]
    if not display:
        print("\nNo tasks found!")
        return
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    display = sorted(display, key=lambda t: priority_order.get(t["priority"], 4))
    print(f"\n{'ID':<5} {'Title':<25} {'Priority':<10} {'Category':<12} {'Status':<10} {'Due Date'}")
    print("-" * 85)
    for t in display:
        status_mark = "DONE" if t["status"] == "Done" else "..."
        category = t.get("category", "N/A")
        print(f"{t['id']:<5} {t['title']:<25} {t['priority']:<10} {category:<12} {status_mark:<10} {t['due_date']}")

def mark_done(tasks):
    view_tasks(tasks, filter_status="Pending")
    try:
        task_id = int(input("\nEnter task ID to mark done: "))
    except ValueError:
        print("Please enter a number!")
        return
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Done":
                print("Task is already done!")
            else:
                task["status"] = "Done"
                save_tasks(tasks)
                print(f"Task '{task['title']}' marked as done!")
            return
    print(f"No task found with ID {task_id}")

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print("Please enter a number!")
        return
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            confirm = input(f"Delete '{task['title']}'? (yes/no): ").lower()
            if confirm in ["yes", "y"]:
                tasks.pop(i)
                save_tasks(tasks)
                print("Task deleted!")
            return
    print(f"No task found with ID {task_id}")

def show_stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "Done")
    pending = total - done
    high = sum(1 for t in tasks if t["priority"] == "High" and t["status"] == "Pending")
    print("\n=== TASK STATISTICS ===")
    print(f"Total Tasks   : {total}")
    print(f"Completed     : {done}")
    print(f"Pending       : {pending}")
    print(f"High Priority : {high} pending")
    if total > 0:
        pct = (done / total) * 100
        print(f"Completion    : {pct:.0f}%")

def show_overdue(tasks):
    today = date.today()
    overdue = []
    for t in tasks:
        if t["status"] == "Done":
            continue
        due = t["due_date"]
        if due == "No due date":
            continue
        try:
            due_dt = datetime.strptime(due, "%Y-%m-%d").date()
            if due_dt < today:
                overdue.append(t)
        except ValueError:
            continue
    if not overdue:
        print("\nNo overdue tasks!")
        return
    view_tasks(overdue)

def show_due_today(tasks):
    today_str = date.today().strftime("%Y-%m-%d")
    due_today = [t for t in tasks if t["due_date"] == today_str and t["status"] != "Done"]
    if not due_today:
        print("\nNo tasks due today!")
        return
    view_tasks(due_today)

def search_tasks(tasks):
    keyword = input("\nEnter keyword to search in title: ").strip().lower()
    if not keyword:
        print("Keyword cannot be empty!")
        return
    results = [t for t in tasks if keyword in t["title"].lower()]
    if not results:
        print("\nNo matching tasks found!")
        return
    view_tasks(results)

def edit_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("\nEnter task ID to edit: "))
    except ValueError:
        print("Please enter a number!")
        return
    for task in tasks:
        if task["id"] == task_id:
            print(f"\nEditing: {task['title']}")
            print("1) Edit title")
            print("2) Edit priority")
            print("3) Edit both")
            choice = input("Select (1-3): ").strip()
            if choice in ["1", "3"]:
                new_title = input("New title: ").strip()
                if new_title:
                    task["title"] = new_title
                else:
                    print("Title left unchanged.")
            if choice in ["2", "3"]:
                print("Priority: 1) High  2) Medium  3) Low")
                while True:
                    p_choice = input("Select (1-3): ").strip()
                    if p_choice == "1":
                        task["priority"] = "High"
                        break
                    elif p_choice == "2":
                        task["priority"] = "Medium"
                        break
                    elif p_choice == "3":
                        task["priority"] = "Low"
                        break
                    else:
                        print("Enter 1, 2, or 3!")
            save_tasks(tasks)
            print("Task updated!")
            return
    print(f"No task found with ID {task_id}")

def main():
    tasks = load_tasks()
    print(f"Loaded {len(tasks)} tasks.")
    while True:
        print("\n=== TO-DO LIST MANAGER ===")
        print("1. Add task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View high priority")
        print("5. Mark task as done")
        print("6. Delete task")
        print("7. Show statistics")
        print("8. Show overdue tasks")
        print("9. Show tasks due today")
        print("10. Search tasks by keyword")
        print("11. Edit task")
        print("12. Exit")
        choice = input("Choose (1-12): ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, filter_status="Pending")
        elif choice == "4":
            view_tasks(tasks, filter_priority="High")
        elif choice == "5":
            mark_done(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            show_stats(tasks)
        elif choice == "8":
            show_overdue(tasks)
        elif choice == "9":
            show_due_today(tasks)
        elif choice == "10":
            search_tasks(tasks)
        elif choice == "11":
            edit_task(tasks)
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()