from .. import (
    ft,
    Optional,
)
from ..gui_elements import (
    HugeLabel,
    MessageLabel,
    InputField,
    InterfaceButton,
)
from ..utils import send_verification_code, SCREEN_SIZE


class PasswordRecoveryPage:
    """Форма страницы восстановления пароля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы восстановления пароля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.email_field = InputField(
            top=414,
            text="Почта",
        )

        self.error_label = MessageLabel(top=580)

    async def on_enter_email(self, action) -> None:
        """Метод обработки заполнения поля ввода email."""
        email = self.email_field.get_value()

        if not email:
            self.error_label.display_error("empty_fields")
            return

        await self.process_send_code(email=email)

    async def process_send_code(self, email: str) -> Optional[Exception]:
        """Метод отправления запроса для получения кода на сервер."""
        try:
            response = await send_verification_code(email=email)

            if response.get("message"):
                self.page.session.set("user_email", email)
                self.clear_fields()
                await self.to_verify(action=None)

            else:
                message = response[list(response.keys())[0]][0]
                self.error_label.display_error(message)

        except Exception as ex:
            return ex

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.email_field.clear()
        self.error_label.clear()
        self.page.update()

    async def to_verify(self, action) -> None:
        """Метод для перехода на страницу для ввода кода верификации."""
        self.page.go("/password-recovery/verify")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            HugeLabel(
                                text="Восстановление\nпароля",
                                top=264,
                            ),
                            self.email_field,
                            self.error_label,
                            InterfaceButton(
                                text="Отправить код",
                                top=670,
                                click=self.on_enter_email,
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
