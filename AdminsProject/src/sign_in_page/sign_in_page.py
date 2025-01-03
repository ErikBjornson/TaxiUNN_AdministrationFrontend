from .. import (
    ft,
    Optional,
)
from ..gui_elements import (
    HugeLabel,
    MessageLabel,
    InputField,
    LinkButton,
    InterfaceButton,
)
from ..utils import dp, send_login_request, SCREEN_SIZE


class SignInPage:
    """Форма страницы авторизации администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы авторизации."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.email_field = InputField(
            top=304,
            text="Почта",
        )

        self.password_field = InputField(
            top=482,
            text="Пароль",
            hint_text="Пароль",
            is_password=True,
        )

        self.error_label = MessageLabel(top=670)

    async def on_login(self, action) -> None:
        """Метод валидации и проверки успешности входа."""
        email = self.email_field.get_value()
        password = self.password_field.get_value()

        if not email or not password:
            self.error_label.display_error("empty_fields")
            return

        await self.process_login(email=email, password=password)

    async def process_login(self, email, password) -> Optional[Exception]:
        """Метод, сохраняющий токен пользователя в сессии страницы."""
        try:
            response = await send_login_request(
                email=email,
                password=password,
            )

            if response.get("access"):
                access_token = response.get("access")

                if access_token:
                    self.page.session.set("access_token", access_token)
                    self.clear_fields()
                    await self.to_profile(action=None)

                else:
                    raise ValueError("Invalid access token.")

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

    async def to_profile(self, action) -> None:
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
                            HugeLabel(
                                text="Вход в аккаунт\nадминистратора",
                                top=144,
                            ),
                            self.email_field,
                            self.password_field,
                            LinkButton(
                                text="Забыли пароль?",
                                top=dp(482) + dp(32) + dp(100),
                                left=dp(566) + dp(28) - dp(10),
                                click=self.to_recovery,
                            ),
                            self.error_label,
                            InterfaceButton(
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
