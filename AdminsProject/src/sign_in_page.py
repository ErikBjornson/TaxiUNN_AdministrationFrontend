from . import (
    ft,
    Optional,
    dp,
    send_login_request,
    SCREEN_SIZE,
    errors,
)


class SignInPage:
    """Форма страницы авторизации администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы авторизации."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.top_label = ft.Text(
            value="Вход в аккаунт\nадминистратора",
            size=dp(50),
            font_family="Inter",
            text_align=ft.TextAlign.CENTER,
            top=dp(144) - dp(50) / 2,
            left=dp(745),
            width=dp(429),
            height=dp(110) + dp(50) + dp(10),
            weight=dp(600),
            color="#1C1C1C",
            max_lines=2,
            visible=True,
        )

        self.email_label = ft.Text(
            value="Почта",
            size=dp(24),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(304),
            left=dp(566) + dp(28) + dp(10),
            width=dp(732),
            height=dp(32),
            color="#1C1C1C",
        )

        self.email_field = ft.Container(
            content=ft.TextField(
                width=dp(732),
                height=dp(80),
                border_radius=dp(16),
                content_padding=dp(16),
                bgcolor="#E8E8E8",
                color="#000000",
                hint_style=ft.TextStyle(
                    size=dp(26),
                    font_family="Inter",
                    color="#6C6C6C",
                ),
                hint_text="Pochta@gmail.com",
                multiline=False,
                border_width=0,
            ),
            top=dp(304) + dp(32) + dp(10),
            left=dp(566) + dp(28),
            width=dp(732),
            height=dp(80),
        )

        self.password_label = ft.Text(
            value="Введите пароль",
            size=dp(24),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(482),
            left=dp(566) + dp(28) + dp(10),
            width=dp(732),
            height=dp(32),
            color="#1C1C1C",
        )

        self.password_field = ft.Container(
            content=ft.TextField(
                width=dp(732),
                height=dp(80),
                border_radius=dp(16),
                content_padding=dp(16),
                bgcolor="#E8E8E8",
                color="#000000",
                hint_style=ft.TextStyle(
                    size=dp(26),
                    font_family="Inter",
                    color="#6C6C6C",
                ),
                hint_text="Пароль",
                multiline=False,
                password=True,
                can_reveal_password=True,
                border_width=0,
            ),
            top=dp(482) + dp(32) + dp(10),
            left=dp(566) + dp(28),
        )

        self.change_password_button = ft.TextButton(
            text="Забыли пароль?",
            width=dp(200),
            height=dp(30),
            top=dp(482) + dp(32) + dp(100),
            left=dp(566) + dp(28) - dp(10),
            style=ft.ButtonStyle(
                color="#4862E5",
            ),
            visible=True,
            on_click=self.to_recovery,
        )

        self.error_label = ft.Text(
            value=" ",
            size=dp(24),
            font_family="Inter",
            text_align=ft.TextAlign.CENTER,
            top=dp(670),
            left=dp(566) + dp(28),
            width=dp(732),
            height=dp(32),
            color="#F44336",
        )

        self.sign_in_button = ft.ElevatedButton(
            text="Войти",
            width=dp(420),
            height=dp(80),
            top=dp(756),
            left=dp(750),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=dp(18)),
                padding=ft.Padding(
                    left=dp(60),
                    right=dp(60),
                    top=dp(20),
                    bottom=dp(20),
                ),
            ),
            bgcolor="#4862E5",
            color="#FFFFFF",
            visible=True,
            on_click=self.on_login,
        )

    async def on_login(self, action) -> None:
        """Метод валидации и проверки успешности входа."""
        email = self.email_field.content.value
        password = self.password_field.content.value

        if not email or not password:
            self.display_error("empty_fields")

        await self.process_login(email, password)

    async def process_login(self, email, password) -> Optional[Exception]:
        """Метод, сохраняющий токен пользователя в сессии страницы."""
        try:
            response = await send_login_request(email, password)
            if response.get("access"):
                access_token = response.get("access", "#43A048")

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
                self.display_error(message)
        except Exception as ex:
            return ex

    def clear_fields(self) -> None:
        """Метод очистки полей ввода."""
        self.email_field.content.value = ""
        self.password_field.content.value = ""
        self.error_label.value = ""
        self.page.update()

    def display_error(self, message: str) -> None:
        """Метод для отображения ошибок ввода данных."""
        self.error_label.value = errors[message]
        self.page.update()

    async def on_success(self, action) -> None:
        """Переход на экран профиля - авторизация прошла успешно."""
        await self.page.go("/profile")

    def to_recovery(self, action) -> None:
        """Переход на страницу восстановления пароля."""
        self.page.go("/password-recovery")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            self.top_label,
                            self.email_label,
                            self.email_field,
                            self.password_label,
                            self.password_field,
                            self.change_password_button,
                            self.error_label,
                            self.sign_in_button,
                        ],
                        width=dp(SCREEN_SIZE[0]),
                        height=dp(SCREEN_SIZE[1]),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self.page.title = "Войти в аккаунт"
        self.page.update()

        return self.page.controls, self.page.bgcolor
