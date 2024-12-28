from .. import ft
from ..utils import dp
from ..gui_elements import InterfaceLabel


class Frame(ft.Container):
    """Класс кнопки-картинки - создаёт группу ft.Image() + ft.Text()."""

    def __init__(
        self,
        image_path: str,
        text: str,
        left: int,
        top: int = 581,
        width: int = 246,
        height: int = 312,
        route: str = None,
    ) -> None:
        """Инициализация группы."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height),
        )

        self.route = route

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=image_path,
                        width=dp(width),
                        height=dp(width),
                        border_radius=ft.border_radius.all(dp(18)),
                        visible=True,
                    ),
                    border=ft.border.all(dp(3)),
                    border_radius=ft.border_radius.all(dp(18)),
                    width=dp(width),
                    height=dp(width),
                    on_click=(self.move_to_page if self.route else None),
                ),
                InterfaceLabel(
                    text=text,
                    size=20,
                    width=width,
                    height=(height - width),
                    align=ft.TextAlign.CENTER,
                    max_lines=2,
                ),
            ],
        )

    def move_to_page(self, action) -> None:
        """Метод перехода на страницу-опцию."""
        self.page.go(self.route)
