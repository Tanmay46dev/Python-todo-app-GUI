import flet as ft
from task import Task
from utils import *


def main(page: ft.Page):
    # Page properties
    page.window_min_width = 600
    page.window_min_height = 600
    page.window_center()
    page.title = "TO-DO App!"
    page.horizontal_alignment = "center"

    # Page related controls
    page.snack_bar = ft.SnackBar(
        content=ft.Text("This is a snack bar"),
        show_close_icon=True,
        duration=1500,
    )

    page.appbar = ft.AppBar(
        title=ft.Row(
            [ft.Icon(ft.icons.CHECKLIST_RTL_OUTLINED), ft.Text("To-do App", size=25, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=PRIMARY_COLOR,
        center_title=True
    )

    # Main controls
    tasks_listview = ft.ListView(
        # first_item_prototype = True,
        expand=True,
        padding=ft.padding.only(left=10, right=10)
    )

    def delete_task(task: Task):
        task_id = task.task_id
        delete_task_from_csv(task_id)
        tasks_listview.controls.remove(task)
        page.snack_bar.content = ft.Text("Todo removed successfully!")
        page.snack_bar.open = True
        page.update()

    # Load the existing tasks from the csv file and display them one by one
    tasks_from_csv = load_tasks_from_csv()
    for task in tasks_from_csv:
        task_string = task.get("task_string")
        task_status = task.get("status")
        task_id = task.get("id")
        tasks_listview.controls.append(Task(task_string, delete_task, task_id, task_status))

    def add_task_to_list(e):
        if not task_field.value:
            return

        task_string = task_field.value
        task_id = tasks_listview.controls[-1].task_id + 1 if tasks_listview.controls else 1

        add_task_to_csv(task_string, task_id)
        tasks_listview.controls.append(Task(task_string, delete_task, task_id))
        task_field.focus()
        task_field.value = ""
        add_task_btn.disabled = True
        page.snack_bar.content = ft.Text("Todo added successfully!")
        page.snack_bar.open = True
        page.update()

    def on_task_field_change(e):
        if task_field.value:
            add_task_btn.disabled = False
        else:
            add_task_btn.disabled = True

        page.update()

    task_field = ft.TextField(
        hint_text="Enter a task to add",
        dense=True,
        on_change=on_task_field_change,
        on_submit=add_task_to_list,
        border_radius=12,
        border_color=PRIMARY_COLOR,
        focused_border_color="white",
        focused_border_width=0.5,
    )

    add_task_btn = ft.IconButton(
        disabled=True,
        bgcolor=PRIMARY_COLOR,
        icon=ft.icons.ADD_OUTLINED,
        on_click=add_task_to_list,
        # icon_color="PRIMARY_COLOR",
        tooltip="Add task"
    )

    page.add(
        # Empty container for space
        ft.Container(height=10),
        # Task input row
        ft.Row(
            controls=[
                task_field,
                ft.Container(width=5),
                add_task_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        # List of all the tasks
        tasks_listview
    )
    page.update()
