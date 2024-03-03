from flet import colors
import csv

PRIMARY_COLOR = colors.PURPLE_900
CSV_FILE_PATH = "tasks.csv"


def load_tasks_from_csv() -> list:
    # Define CSV file path

    # Read tasks from CSV and store them in a list as dictionaries
    tasks_list = []
    with open(CSV_FILE_PATH, mode="r", newline="\n", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            # Convert 'id' and 'status' values to appropriate types
            row["id"] = int(row["id"])
            row["status"] = row["status"].lower() == "true"

            # Append the formatted task dictionary to the list
            tasks_list.append({
                "task_string": row["task_string"],
                "id": row["id"],
                "status": row["status"]
            })
    return tasks_list


def add_task_to_csv(task_string, task_id, task_status=False):
    # Append the new task to the CSV file
    with open(CSV_FILE_PATH, mode="a", newline="\n", encoding="utf-8") as csv_file:
        fieldnames = ["task_string", "id", "status"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # If the file is empty, write the header
        if csv_file.tell() == 0:
            writer.writeheader()

        # Write the new task
        writer.writerow({
            "task_string": task_string,
            "id": task_id,
            "status": task_status
        })


def delete_task_from_csv(task_id: int):
    # Read existing tasks from CSV
    tasks = load_tasks_from_csv()

    # Find and remove the task with the specified task_id
    tasks = [task for task in tasks if task["id"] != task_id]

    # Write the updated tasks back to the CSV file
    with open(CSV_FILE_PATH, mode="w", newline="\n", encoding="utf-8") as csv_file:
        fieldnames = ["task_string", "id", "status"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write tasks
        writer.writerows(tasks)


def update_task(task_id, new_task_string: str = "", new_task_status: bool = None):
    tasks = load_tasks_from_csv()

    for task in tasks:
        if task["id"] == task_id:
            if new_task_string:
                task["task_string"] = new_task_string
            if new_task_status != None:
                task["status"] = new_task_status

    # Write the updated tasks back to the CSV file
    with open(CSV_FILE_PATH, mode="w", newline="\n", encoding="utf-8") as csv_file:
        fieldnames = ["task_string", "id", "status"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write tasks
        writer.writerows(tasks)
