from . import (
    ft,
    dp,
    SCREEN_SIZE,
    TopLabel,
    InterfaceLabel,
    InputField,
    EnterButton,
)


class PasswordRecoveryPage:
    """Форма страницы восстановления пароля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы восстановления пароля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.email_field = InputField(
            hint_text="Pochta@gmail.com",
            is_password=False,
            top=dp(414) + dp(32) + dp(10),
        )

        self.error_label = InterfaceLabel(
            value=" ",
            top=580,
            align=ft.TextAlign.CENTER,
            color="#F44336",
        )

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.email_field.clear()
        self.error_label.clear()

        self.page.update()

    def to_verify_page(self, action) -> None:
        """Метод для перехода на страницу для ввода кода верификации."""
        if not self.email_field.get_value():
            self.error_label.display_error("empty_fields")
            return

        self.clear_fields()
        self.page.go("/password-recovery/verify")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            TopLabel(
                                value="Восстановление\nпароля",
                                top=264,
                            ),
                            InterfaceLabel(
                                value="Почта",
                                top=414,
                            ),
                            self.email_field,
                            self.error_label,
                            EnterButton(
                                text="Отправить код",
                                top=670,
                                click=self.to_verify_page,
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
        self.page.title = "Восстановление пароля"
        self.page.update()

        return self.page.controls, self.page.bgcolor
