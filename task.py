import flet as ft
from utils import PRIMARY_COLOR, update_task


class Task(ft.UserControl):
    def __init__(self, task_string: str, delete_task, task_id: int, status=False) -> None:
        super().__init__()
        self.delete_task = delete_task
        self.task_id = task_id
        self.task_checkbox = ft.Checkbox(
            label=task_string,
            value=status,
            check_color=PRIMARY_COLOR,
            on_change=self.on_task_checkbox_change,
        )

        self.edit_btn = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color=PRIMARY_COLOR,
            on_click=self.edit_btn_clicked,
            tooltip="Edit task"
        )

        self.delete_btn = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color=ft.colors.RED_900,
            tooltip="Delete task",
            on_click=self.delete_btn_clicked
        )

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.task_checkbox,
                ft.Row(
                    spacing=0,
                    controls=[
                        self.edit_btn,
                        self.delete_btn
                    ]
                )
            ],
        )

        self.edit_field = ft.TextField(
            expand=1,
            dense=True,
            value=self.task_checkbox.label,
            on_submit=self.edit_task,
            border_radius=12,
            focused_border_color=PRIMARY_COLOR,
            border_color="white",
            focused_border_width=0.5,
        )
        
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_field,
                ft.IconButton(
                    icon=ft.icons.CHECK_CIRCLE_OUTLINE,
                    icon_color=PRIMARY_COLOR,
                    tooltip="Update To-Do",
                    on_click=self.edit_task,
                ),
            ],
        )

        self.task_control = ft.Column(
            controls=[
                self.display_view,
                self.edit_view
            ],

        )

    def on_task_checkbox_change(self, e):
        update_task(self.task_id, new_task_status=self.task_checkbox.value)

    def delete_btn_clicked(self, e):
        self.delete_task(self)

    def edit_task(self, e):
        new_task_string = self.edit_field.value
        self.task_checkbox.label = new_task_string
        update_task(self.task_id, new_task_string=new_task_string)
        self.edit_view.visible = False
        self.update()

    def edit_btn_clicked(self, e):
        self.edit_view.visible = not self.edit_view.visible
        self.edit_field.focus()
        self.update()

    def build(self):
        return self.task_control
