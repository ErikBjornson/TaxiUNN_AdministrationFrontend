from . import (
    ft,
    SCREEN_SIZE,
    HugeLabel,
    MessageLabel,
    InterfaceButton,
    InputField,
    GoBackButton,
)


class AddAdminsPage:
    """Форма страницы для добавления новых администраторов."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы добавления администраторов."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.full_name_field = InputField(
            top=317,
            text="Имя Фамилия",
            hint_text="Иван Иванов",
            is_password=False,
        )
        self.email_field = InputField(
            top=500,
            text="Почта",
            hint_text="Pochta@gmail.com",
            is_password=False,
        )
        self.error_label = MessageLabel(top=670)

    def clear_fields(self, action) -> None:
        """Метод очистки полей ввода и надписей."""
        self.full_name_field.clear()
        self.email_field.clear()
        self.error_label.clear()
        self.page.update()

    def add_admin(self, action) -> None:
        """Метод обработки события нажатия на кнопку 'Добавить'."""
        full_name = self.full_name_field.get_value()
        email = self.email_field.get_value()

        if not full_name or not email:
            self.error_label.display_error("empty_fields")
            return

    def to_profile(self, action) -> None:
        """Метод возвращения на страницу профиля."""
        self.clear_fields(action=None)
        self.page.go("/profile")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            GoBackButton(
                                text="Меню",
                                click=self.to_profile,
                            ),
                            HugeLabel(
                                text="Добавление нового\nадминистратора",
                                top=144,
                            ),
                            self.full_name_field,
                            self.email_field,
                            self.error_label,
                            InterfaceButton(
                                text="Добавить",
                                top=750,
                                click=self.add_admin,
                                left=677,
                                width=265,
                            ),
                            InterfaceButton(
                                text="Очистить",
                                top=750,
                                click=self.clear_fields,
                                left=970,
                                width=265,
                                text_color="#1C1C1C",
                                bgcolor="#FFFFFF",
                            ),
                        ],
                        width=SCREEN_SIZE[0],
                        height=SCREEN_SIZE[1],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self.page.title = "Добавление новых администраторов"
        self.page.update()

        return self.page.controls, self.page.bgcolor
