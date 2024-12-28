from .. import ft
from ..utils import dp, SCREEN_SIZE
from ..gui_elements import (
    HugeLabel,
    GrayLabel,
    InterfaceButton,
)


class WelcomePage:
    """Форма приветственной страницы."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация приветственной страницы."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

    def to_sign_in(self, action) -> None:
        """Переход на экран авторизации - уход с приветственной страницы."""
        self.page.go("/login")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Row(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(
                                src="../assets/welcomePageImage.png",
                                width=dp(1400),
                                height=dp(1050),
                                top=dp(-42),
                                left=dp(-93),
                            ),
                            HugeLabel(
                                text="Добро пожаловать",
                                size=77,
                                top=350,
                                left=1200,
                                align=ft.TextAlign.LEFT,
                            ),
                            GrayLabel(
                                text="Сервис для администрирования такси",
                                top=540,
                                left=1200,
                                size=26,
                                align=ft.TextAlign.LEFT,
                                width=500,
                                height=55,
                                weight=500,
                            ),
                            InterfaceButton(
                                text="Войти в аккаунт",
                                click=self.to_sign_in,
                                top=655,
                                left=1200,
                                width=520,
                                height=85,
                            ),
                        ],
                        width=SCREEN_SIZE[0],
                        height=SCREEN_SIZE[1],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
        self.page.title = "Добро пожаловать!"
        self.page.update()

        return self.page.controls, self.page.bgcolor
