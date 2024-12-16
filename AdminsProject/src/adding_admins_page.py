from . import (
    ft,
    dp,
    SCREEN_SIZE,
    TopLabel,
    InterfaceLabel,
    InputField,
    EnterButton,
    GoBackButton,
)


class AddAdminsPage:
    """Форма страницы для добавления новых администраторов."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы добавления администраторов."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.full_name_field = InputField(
            hint_text="Иван Иванов",
            is_password=False,
            top=dp(317) + dp(32) + dp(10),
        )
        self.email_field = InputField(
            hint_text="Pochta@gmail.com",
            is_password=False,
            top=dp(500) + dp(32) + dp(10),
        )
        self.error_label = InterfaceLabel(
            value=" ",
            top=670,
            align=ft.TextAlign.CENTER,
            color="#F44336",
        )

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
                            TopLabel(
                                value="Добавление нового\nадминистратора",
                                top=144,
                            ),
                            InterfaceLabel(
                                value="Имя Фамилия",
                                top=317,
                            ),
                            self.full_name_field,
                            InterfaceLabel(
                                value="Почта",
                                top=500,
                            ),
                            self.email_field,
                            self.error_label,
                            EnterButton(
                                text="Добавить",
                                top=750,
                                click=self.add_admin,
                                left=677,
                                width=265,
                            ).fset_color(
                                bgcolor="#4862E5",
                                text_color="#FFFFFF",
                            ),
                            EnterButton(
                                text="Очистить",
                                top=750,
                                click=self.clear_fields,
                                left=970,
                                width=265,
                            ).fset_color(
                                bgcolor="#FFFFFF",
                                text_color="#1C1C1C",
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
