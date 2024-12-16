from . import ft, dp, errors


class BaseLabel(ft.Text):
    """Базовый класс надписей."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__()
        self.size = dp(24)
        self.font_family = "Inter"
        self.text_align = ft.TextAlign.CENTER
        self.color = "#1C1C1C"


class TopLabel(BaseLabel):
    """Класс заголовочной надписи страницы."""

    def __init__(self, value: str, top: int) -> None:
        """Инициализация класса надписи."""
        super().__init__()
        self.value = value
        self.size = dp(50)
        self.top = dp(top) - dp(50) / 2
        self.left = dp(665)
        self.width = dp(600)
        self.height = dp(110) + dp(50) + dp(10)
        self.weight = dp(600)
        self.max_lines = 2


class GrayLabel(BaseLabel):
    """Класс надписи-подсказки серого цвета."""

    def __init__(
        self,
        value: str,
        sizes: list[int],
        top: int,
        left: int = 760,
    ) -> None:
        """Инициализация класса надписи."""
        super().__init__()
        self.value = value
        self.max_lines = 2
        self.width = dp(sizes[0])
        self.height = dp(sizes[1])
        self.weight = dp(sizes[2])
        self.top = dp(top) - dp(24) / 2
        self.left = dp(left)
        self.color = "#A0A0A0"
        self.size = dp(sizes[3])


class InterfaceLabel(BaseLabel):
    """Вспомогательный класс - отображает надписи при валидации и вводе."""

    def __init__(
        self,
        value: str,
        top: int,
        align: ft.TextAlign = ft.TextAlign.LEFT,
        color: str = "#1C1C1C",
    ) -> None:
        """Инициализация вспомогательного класса."""
        super().__init__()
        self.value = value
        self.text_align = align
        self.top = dp(top)
        self.left = dp(566) + dp(28)
        self.width = dp(732)
        self.height = dp(32)
        self.color = color

    def display_error(self, message: str) -> None:
        """Метод для отображения ошибок ввода данных."""
        self.color = "#F44336"
        self.value = errors[message]
        self.page.update()

    def display_system_message(self, message: str) -> None:
        """Метод для отображения системных сообщений."""
        self.color = "#43A048"
        self.value = message
        self.page.update()

    def clear(self) -> None:
        """Метод очистки надписи."""
        self.value = ""


class InputField(ft.Container):
    """Вспомогательный класс - отображает поле ввода данных пользователя."""

    def __init__(self, hint_text: str, is_password: bool, top: float) -> None:
        """Инициализация вспомогательного класса."""
        super().__init__()
        self.content = ft.TextField(
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
            hint_text=hint_text,
            multiline=False,
            password=is_password,
            can_reveal_password=is_password,
            border_width=0,
        )
        self.top = top
        self.left = dp(566) + dp(28)
        self.width = dp(732)
        self.height = dp(80)

    def get_value(self) -> str:
        """Метод get для введённого значения."""
        return self.content.value

    def clear(self) -> None:
        """Метод очистки поля ввода."""
        self.content.value = ""


class BaseButton(ft.ElevatedButton):
    """Базовый класс кнопки интерфейса."""

    def __init__(self) -> None:
        """Инициализация базового класса."""
        super().__init__()
        self.height = dp(80)
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=dp(18)),
            padding=ft.Padding(
                left=dp(60),
                right=dp(60),
                top=dp(20),
                bottom=dp(20),
            ),
            side=ft.BorderSide(
                width=dp(3),
                color="#4862E5",
            ),
        )
        self.bgcolor = "#4862E5"
        self.color = "#FFFFFF"


class EnterButton(BaseButton):
    """Кнопка ввода данных (и перехода на следующую страницу)."""

    def __init__(
        self,
        text: str,
        top: int,
        click,
        left: int = 750,
        width: int = 420,
    ) -> None:
        """Инициализация кнопки."""
        super().__init__()
        self.text = text
        self.width = dp(width)
        self.top = dp(top)
        self.left = dp(left)
        self.on_click = click

    def fset_color(self, bgcolor: str, text_color: str):
        """Метод стилизации кнопки."""
        self.bgcolor = bgcolor
        self.color = text_color
        return self


class LinkButton(ft.TextButton):
    """Класс ссылочной кнопки (с текстом синего цвета, похожа на ссылку)."""

    def __init__(
        self,
        text: str,
        top: float,
        left: float,
        click,
        width: int = 200,
    ) -> None:
        """Инициализация ссылочной кнопки."""
        super().__init__()
        self.text = text
        self.style = ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=dp(18),
                font_family="Inter",
            ),
        )
        self.width = dp(width)
        self.height = dp(30)
        self.top = top
        self.left = left
        self.style = ft.ButtonStyle(
            color="#4862E5",
        )
        self.on_click = click


class GoBackButton(ft.ElevatedButton):
    """Класс кнопки возвращения на предыдущую страницу."""

    def __init__(self, text: str, click) -> None:
        """Инициализация класса кнопки."""
        super().__init__()
        self.color = "#000000"
        self.bgcolor = "#FFFFFF"
        self.width = dp(230)
        self.height = dp(60)
        self.top = dp(80)
        self.left = dp(160)
        self.elevation = 0
        self.content = ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.CHEVRON_LEFT,
                    size=dp(40),
                ),
                ft.Text(
                    value=text,
                    size=dp(25),
                    font_family="Inter",
                    text_align=ft.TextAlign.LEFT,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.on_click = click
