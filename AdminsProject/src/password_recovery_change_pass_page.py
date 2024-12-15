from . import (
    ft,
    Optional,
    dp,
    change_password,
    SCREEN_SIZE,
    TopLabel,
    GrayLabel,
    InterfaceLabel,
    InputField,
    EnterButton,
)


class ChangePasswordPage:
    """Форма страницы для установления нового пароля после верификации."""

    def __init__(self, page: ft.Page) -> None:
        """Метод инициализации страницы установления нового пароля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.gray_label = GrayLabel(
            value="Пароль должен содержать\nне менее 8 знаков",
            sizes=[380, 62, 400, 24],
            top=290,
            left=770,
        )

        self.first = InputField(
            hint_text="Пароль",
            is_password=True,
            top=dp(370) + dp(32) + dp(10),
        )

        self.second = InputField(
            hint_text="Пароль",
            is_password=True,
            top=dp(532) + dp(32) + dp(10),
        )

        self.error_label = InterfaceLabel(
            value=" ",
            top=690,
            align=ft.TextAlign.CENTER,
            color="#F44336",
        )

    def is_passwords_equals(self) -> bool:
        """Метод проверки, что два введённых пароля верны."""
        return self.first.get_value() == self.second.get_value()

    async def on_change_password(self, action) -> None:
        """Метод обработки заполнения полей создания и подтверждения пароля."""
        first = self.first.get_value()
        second = self.second.get_value()

        if not first or not second:
            self.error_label.display_error("empty_fields")
            return

        if not self.is_passwords_equals():
            self.error_label.display_error("different_passwords")
            return

        if len(first) < 8:
            self.error_label.display_error("to_short_passwords")
            return

        await self.process_change(new_password=first)

    async def process_change(self, new_password) -> Optional[Exception]:
        """Метод отправки запроса о смене пароля на сервер."""
        try:
            response = await change_password(
                email=self.page.session.get("user_email"),
                new_password=new_password,
            )
            if response.get("message"):
                self.page.session.remove("user_email")
                self.clear_fields()
                await self.to_login(action=None)
            else:
                message = response[list(response.keys())[0]][0]
                self.error_label.display_error(message)
        except Exception as ex:
            return ex

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""
        self.first.clear()
        self.second.clear()
        self.error_label.clear()
        self.page.update()

    async def to_login(self, action) -> None:
        """Метод возвращения на страницу авторизации после смены пароля."""
        self.page.go("/login")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод для отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            TopLabel(
                                value="Установите\nновый пароль",
                                top=144,
                            ),
                            self.gray_label,
                            InterfaceLabel(
                                value="Введите пароль",
                                top=370,
                            ),
                            self.first,
                            InterfaceLabel(
                                value="Подтвердите пароль",
                                top=532,
                            ),
                            self.second,
                            self.error_label,
                            EnterButton(
                                text="Сохранить пароль",
                                top=770,
                                click=self.on_change_password,
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
        self.page.title = "Сменить пароль"
        self.page.update()

        return self.page.controls, self.page.bgcolor
