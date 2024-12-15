from . import (
    ft,
    Optional,
    dp,
    send_verification_code,
    do_verification,
    SCREEN_SIZE,
    TopLabel,
    GrayLabel,
    InterfaceLabel,
    EnterButton,
    LinkButton,
)


class VerificationCodeInput(ft.Container):
    """Вспомогательный класс - создаёт поле ввода для кода верификации."""

    def __init__(self) -> None:
        """Инициализация кастомного поля ввода."""
        super().__init__()
        self.content = ft.Stack(
            controls=[
                ft.Column(
                    controls=[
                        ft.TextField(
                            width=dp(70),
                            height=dp(90),
                            border_color="#4862E5",
                            border_radius=dp(10),
                            border_width=dp(3),
                            bgcolor="#FFFFFF",
                            color="#000000",
                            multiline=False,
                            max_lines=1,
                            on_change=self.to_next,
                            on_focus=self.to_last_entered,
                            text_align=ft.TextAlign.CENTER,
                            text_style=ft.TextStyle(
                                size=dp(30),
                                font_family="Inter",
                            ),
                        ),
                    ],
                    width=dp(70),
                    height=dp(90),
                    left=dp(20) + dp(106) * index,
                ) for index in range(5)
            ],
            width=dp(530),
            height=dp(90),
        )

        self.index = 0
        self.array = self.content.controls
        self.values = ""

        self.top = dp(471)
        self.left = dp(695)
        self.width = dp(530)
        self.height = dp(90)

    def fget_section(self, index: int) -> None:
        """Метод get для получения доступа к ячейке по индексу."""
        return self.array[index].controls[0]

    def fset_section(self, index: int, value: str = "") -> None:
        """Метод set для очистки ячеек."""
        self.fget_section(index).value = value

    def get_value_of_section(self, index: int) -> None:
        """Метод get для получения значения ячейки по индексу."""
        return self.fget_section(index).value

    def get_code(self) -> str:
        """Метод get для вводимого кода - используется для валидации."""
        return self.values

    def to_last_entered(self, action) -> None:
        """Метод переводит курсор на последнюю незаполненную ячейку."""
        index = 0 if self.index == 0 else self.index

        self.fget_section(index).focus()

    def to_next(self, action) -> None:
        """Метод перехода к следующей ячейке, если текущая уже заполнена."""
        self.values += self.get_value_of_section(self.index)

        if self.index < 4:
            self.fget_section(self.index + 1).focus()
            self.index += 1

    def clear_sections(self) -> None:
        """Метод очистки ячеек."""
        self.values = ""
        for index in range(5):
            self.fset_section(index)
        self.index = 0
        self.to_last_entered(action=None)


class PasswordRecoveryVerifyPage:
    """Форма страницы для ввода кода верификации для восстановления пароля."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы верификации."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.verification_code_input = VerificationCodeInput()

        self.error_label = InterfaceLabel(
            value=" ",
            top=590,
            align=ft.TextAlign.CENTER,
            color="#F44336",
        )

    async def on_enter_code(self, action) -> None:
        """Метод обработки ввода кода верификации."""
        code = self.verification_code_input.get_code()

        if not code or len(code) < 5:
            self.error_label.display_error("empty_fields")
            return

        await self.process_verify(verification_code=code)

    async def process_verify(self, verification_code) -> Optional[Exception]:
        """Метод отправки запроса для перехода к смене пароля на сервер."""
        try:
            response = await do_verification(
                email=self.page.session.get("user_email"),
                verification_code=verification_code,
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
        self.error_label.display_system_message(
            "Новый код отправлен на вашу почту",
        )
        await send_verification_code(
            email=self.page.session.get("user_email"),
        )

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.verification_code_input.clear_sections()
        self.error_label.clear()
        self.page.update()

    async def to_change_password(self, action) -> None:
        """Метод перехода на страницу смены пароля администратора."""
        self.page.go("/password-recovery/change")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        email = f"на почту {self.page.session.get('user_email')}"

        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            TopLabel(
                                value="Введите\nпятизначный код",
                                top=194,
                            ),
                            GrayLabel(
                                value=f"Код подтверждения отправлен\n{email}",
                                sizes=[800, 70, 400, 24],
                                top=334,
                                left=560,
                            ),
                            self.verification_code_input,
                            self.error_label,
                            EnterButton(
                                text="Продолжить",
                                top=683,
                                click=self.on_enter_code,
                            ),
                            GrayLabel(
                                value="Код не пришёл?",
                                sizes=[180, 30, 250, 21],
                                top=790,
                                left=760,
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
