from . import (
    ft,
    Optional,
    dp,
    send_login_request,
    SCREEN_SIZE,
    TopLabel,
    InterfaceLabel,
    InputField,
    LinkButton,
    EnterButton,
)


class SignInPage:
    """Форма страницы авторизации администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы авторизации."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.email_field = InputField(
            hint_text="Pochta@gmail.com",
            is_password=False,
            top=dp(304) + dp(32) + dp(10),
        )

        self.password_field = InputField(
            hint_text="Пароль",
            is_password=True,
            top=dp(482) + dp(32) + dp(10),
        )

        self.error_label = InterfaceLabel(
            value=" ",
            top=670,
            align=ft.TextAlign.CENTER,
            color="#F44336",
        )

    async def on_login(self, action) -> None:
        """Метод валидации и проверки успешности входа."""
        email = self.email_field.content.value
        password = self.password_field.content.value

        if not email or not password:
            self.error_label.display_error("empty_fields")

        await self.process_login(email, password)

    async def process_login(self, email, password) -> Optional[Exception]:
        """Метод, сохраняющий токен пользователя в сессии страницы."""
        try:
            response = await send_login_request(email, password)
            if response.get("access"):
                access_token = response.get("access")

                if access_token:
                    self.page.session.set("access_token", access_token)
                    self.clear_fields()

                    await self.on_success(
                        action=None,
                    )

                else:
                    raise ValueError("Invalid access token!")

            else:
                message = response[list(response.keys())[0]][0]
                self.error_label.display_error(message)
        except Exception as ex:
            return ex

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.email_field.clear()
        self.password_field.clear()
        self.error_label.clear()

        self.page.update()

    async def on_success(self, action) -> None:
        """Переход на экран профиля - авторизация прошла успешно."""
        await self.page.go("/profile")

    def to_recovery(self, action) -> None:
        """Переход на страницу восстановления пароля."""
        self.clear_fields()
        self.page.go("/password-recovery")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            TopLabel(
                                value="Вход в аккаунт\nадминистратора",
                                top=144,
                            ),
                            InterfaceLabel(
                                value="Почта",
                                top=304,
                            ),
                            self.email_field,
                            InterfaceLabel(
                                value="Введите пароль",
                                top=482,
                            ),
                            self.password_field,
                            LinkButton(
                                text="Забыли пароль?",
                                top=dp(482) + dp(32) + dp(100),
                                left=dp(566) + dp(28) - dp(10),
                                click=self.to_recovery,
                            ),
                            self.error_label,
                            EnterButton(
                                text="Войти",
                                top=750,
                                click=self.on_login,
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
        self.page.title = "Войти в аккаунт"
        self.page.update()

        return self.page.controls, self.page.bgcolor
