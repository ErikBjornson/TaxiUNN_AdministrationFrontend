from .. import (
    ft,
    Optional,
)
from ..gui_elements import (
    HugeLabel,
    GrayLabel,
    MessageLabel,
    InterfaceButton,
    LinkButton,
)
from ..utils import (
    dp,
    send_verification_code,
    do_verification,
    SCREEN_SIZE,
)
from .verification_code_input import VerificationCodeInput


class PasswordRecoveryVerifyPage:
    """Форма страницы для ввода кода верификации для восстановления пароля."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы верификации."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.vci = VerificationCodeInput()

        self.error_label = MessageLabel(top=590)

    async def on_enter_code(self, action) -> None:
        """Метод обработки ввода кода верификации."""
        code = self.vci.get_code()

        if not code or len(code) < 5:
            self.error_label.display_error("empty_fields")
            return

        await self.process_verify(code=code)

    async def process_verify(self, code: str) -> Optional[Exception]:
        """Метод отправки запроса для перехода к смене пароля на сервер."""
        try:
            response = await do_verification(
                email=self.page.session.get("user_email"),
                verification_code=code,
            )

            if response.get("message"):
                self.clear_fields()
                await self.to_change_password(action=None)

            else:
                message = response[list(response.keys())[0]][0]
                self.error_label.display_error(message)

        except Exception as ex:
            return ex

    async def send_new_code(self, action) -> None:
        """Метод отправки другого кода верификации."""
        self.error_label.display_success(
            "Новый код отправлен на вашу почту",
        )
        await send_verification_code(
            email=self.page.session.get("user_email"),
        )

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.vci.clear_sections()
        self.error_label.clear()
        self.page.update()

    async def to_change_password(self, action) -> None:
        """Метод перехода на страницу смены пароля администратора."""
        self.page.go("/password-recovery/change")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            HugeLabel(
                                text="Введите\nпятизначный код",
                                top=194,
                            ),
                            GrayLabel(
                                text=(
                                    "Код подтверждения отправлен\nна почту "
                                    f"{self.page.session.get('user_email')}"
                                ),
                                top=334,
                            ),
                            self.vci,
                            self.error_label,
                            InterfaceButton(
                                text="Продолжить",
                                top=683,
                                click=self.on_enter_code,
                            ),
                            GrayLabel(
                                text="Код не пришёл?",
                                top=778,
                                left=760,
                                size=21,
                                width=180,
                                height=30,
                                weight=250,
                            ),
                            LinkButton(
                                text="Отправить заново",
                                top=dp(778),
                                left=dp(760) + dp(180),
                                click=self.send_new_code,
                                width=220,
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
        self.page.title = "Введите код верификации"
        self.page.update()

        return self.page.controls, self.page.bgcolor
