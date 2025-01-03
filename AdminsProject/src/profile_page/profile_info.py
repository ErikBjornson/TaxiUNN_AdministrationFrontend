from .. import ft
from ..utils import dp
from ..gui_elements import InterfaceLabel


class ProfileInfo(ft.Container):
    """Класс, создающий поле 'Имя Фамилия' и поле с почтой."""

    def __init__(
        self,
        top: int = 300,
        left: int = 737,
        width: int = 400,
        height: int = 90,
    ) -> None:
        """Инициализация группы."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height),
        )

        self.content = ft.Column(
            controls=[
                InterfaceLabel(
                    text=" ",
                    size=40,
                    width=width,
                    height=50,
                    align=ft.TextAlign.CENTER,
                ),
                InterfaceLabel(
                    text=" ",
                    size=24,
                    width=width,
                    height=35,
                    color="#A0A0A0",
                    align=ft.TextAlign.CENTER,
                ),
            ],
        )

    def update_profile_info(self, name: str, login: str) -> None:
        """Заполнение данных профиля."""
        self.content.controls[0].value = name
        self.content.controls[1].value = login
        self.page.update()
