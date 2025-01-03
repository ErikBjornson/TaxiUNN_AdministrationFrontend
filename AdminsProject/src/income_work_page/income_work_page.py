from .. import ft
from ..utils import SCREEN_SIZE
from ..gui_elements import GoBackButton


class IncomeWorkPage:
    """Форма страницы работы с доходами."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы работы с доходами."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

    def to_profile(self, action) -> None:
        """Метод возвращения на страницу профиля."""
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
                                click=self.to_profile,
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
        self.page.title = "Работа с доходами сотрудников"
        self.page.update()

        return self.page.controls, self.page.bgcolor
