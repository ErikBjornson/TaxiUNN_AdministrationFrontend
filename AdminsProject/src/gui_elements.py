from . import ft
from .utils import dp, errors


class HugeLabel(ft.Text):
    """Класс крупной надписи интерфейса."""

    def __init__(
        self,
        text: str,
        top: int,
        left: int = 665,
        align: ft.TextAlign = ft.TextAlign.CENTER,
        max_lines: int = 2,
    ) -> None:
        """Инициализация крупной надписи интерфейса."""
        super().__init__(
            value=text,
            top=dp(top) - dp(50) / 2,
            left=dp(left),
            width=dp(600),
            height=dp(110) + dp(50) + dp(10),
            weight=dp(600),
            text_align=align,
            max_lines=max_lines,
        )
        self.style = ft.TextStyle(
            font_family="Inter",
            size=dp(50),
        )
        self.color = "#000000"


class GrayLabel(ft.Text):
    """Класс серой надписи (надписи-подсказки) интерфейса."""

    def __init__(
        self,
        text: str,
        top: int,
        left: int = 560,
        size: int = 24,
        align: ft.TextAlign = ft.TextAlign.CENTER,
        width: int = 800,
        height: int = 70,
        weight: int = 500,
        max_lines: int = 2,
    ) -> None:
        """Инициализация класса серой надписи."""
        super().__init__(
            value=text,
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height) + dp(size) + dp(10),
            weight=dp(weight),
            text_align=align,
            max_lines=max_lines,
        )
        self.style = ft.TextStyle(
            font_family="Inter",
            size=dp(size),
        )
        self.color = "#A0A0A0"


class MessageLabel(ft.Text):
    """Класс надписи-сообщения (отображает ошибки или успешное действие)."""

    def __init__(
        self,
        top: int,
    ) -> None:
        """Инициализация класса надписи-сообщения."""
        super().__init__(
            top=dp(top),
            left=dp(566) + dp(28),
            width=dp(732),
            height=dp(32),
            text_align=ft.TextAlign.CENTER,
        )
        self.value = " "
        self.style = ft.TextStyle(
            font_family="Inter",
            size=dp(24),
        )

    def display_error(self, message: str) -> None:
        """Метод для отображения ошибок ввода данных."""
        self.color = "#F44336"
        self.value = errors[message]
        self.page.update()

    def display_success(self, message: str) -> None:
        """Метод для отображения системных сообщений."""
        self.color = "#43A048"
        self.value = message
        self.page.update()

    def clear(self) -> None:
        """Метод очистки надписи."""
        self.value = ""


class InterfaceLabel(ft.Text):
    """Класс простой надписи."""

    def __init__(
        self,
        text: str,
        size: int,
        width: int,
        height: int,
        color: str = "#1C1C1C",
        align: ft.TextAlign = ft.TextAlign.LEFT,
    ) -> None:
        """Инициализация класса простой надписи."""
        super().__init__(
            value=text,
            font_family="Inter",
            size=dp(size),
            color=color,
            width=dp(width),
            height=dp(height),
            text_align=align,
        )


class InterfaceField(ft.TextField):
    """Класс простого поля ввода."""

    def __init__(
        self,
        size: int = 26,
        width: int = 732,
        height: int = 80,
        hint_text: str = "",
        suffix: str = "",
        is_password: bool = False,
        field_id: str = "",
    ) -> None:
        """Инициализация класса простого поля ввода."""
        super().__init__(
            width=dp(width),
            height=dp(height),
            hint_text=hint_text,
            suffix_text=suffix,
            password=is_password,
            can_reveal_password=is_password,
            bgcolor="#E8E8E8",
            color="#000000",
            border_radius=dp(16),
            content_padding=dp(16),
            multiline=False,
            border_width=0,
        )
        self.field_id = field_id
        self.hint_style = ft.TextStyle(
            font_family="Inter",
            size=dp(size),
            color="#6C6C6C",
        )
        self.suffix_style = ft.TextStyle(
            font_family="Inter",
            size=dp(size),
            color="#1C1C1C",
        )
        self.on_change = self.readings

    def readings(self, action) -> None:
        """Метод для записи вводимых значений в сессию страницы."""
        if self.field_id:
            self.page.session.set(f"{self.field_id}", self.value)


class InputField(ft.Container):
    """Класс поля ввода данных пользователя."""

    def __init__(
        self,
        top: int,
        left: int | None = 600,
        text: str = " ",
        size: int = 26,
        width: int = 732,
        entry_height: int = 80,
        hint_text: str = "Pochta@gmail.com",
        is_password: bool = False,
    ) -> None:
        """Инициализация класса поля ввода данных пользователя."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(30) + dp(entry_height),
        )
        self.content = ft.Column(
            controls=[
                InterfaceLabel(
                    text=text,
                    size=22,
                    width=width,
                    height=30,
                ),
                InterfaceField(
                    size=size,
                    width=width,
                    height=entry_height,
                    hint_text=hint_text,
                    is_password=is_password,
                ),
            ],
        )

    def get_value(self) -> str:
        """Метод get для введённого значения."""
        return self.content.controls[1].value

    def clear(self) -> None:
        """Метод очистки поля ввода."""
        self.content.controls[1].value = ""


class InterfaceButton(ft.ElevatedButton):
    """Класс кнопки интерфейса."""

    def __init__(
        self,
        text: str,
        click: callable,
        top: int | None = 750,
        left: int | None = 750,
        width: int = 420,
        height: int = 80,
        text_size: int = 24,
        text_color: str = "#FFFFFF",
        bgcolor: str = "#4862E5",
        border_color: str = "#4862E5",
    ) -> None:
        """Инициализация класса кнопки интерфейса."""
        super().__init__(
            text=text,
            width=dp(width),
            height=dp(height),
            top=dp(top),
            left=dp(left),
            color=text_color,
            bgcolor=bgcolor,
            on_click=click,
        )
        self.style = ft.ButtonStyle(
            text_style=ft.TextStyle(
                font_family="Inter",
                size=dp(text_size),
            ),
            shape=ft.RoundedRectangleBorder(radius=dp(18)),
            side=ft.BorderSide(
                width=dp(3),
                color=border_color,
            ),
        )


class LinkButton(ft.TextButton):
    """Класс кнопки-ссылки (с текстом синего цвета, похожа на ссылку)."""

    def __init__(
        self,
        text: str,
        top: float,
        left: float,
        click: callable,
        width: int = 200,
    ) -> None:
        """Инициализация класса кнопки-ссылки."""
        super().__init__(
            text=text,
            top=top,
            left=left,
            width=dp(width),
            height=dp(30),
            on_click=click,
        )
        self.style = ft.ButtonStyle(
            color="#4862E5",
        )


class GoBackButton(ft.ElevatedButton):
    """Класс кнопки возвращения на предыдущую страницу."""

    def __init__(self, text: str, click: callable) -> None:
        """Инициализация класса кнопки."""
        super().__init__(
            top=dp(80),
            left=dp(160),
            width=dp(230),
            height=dp(60),
            elevation=0,
            color="#000000",
            bgcolor="#FFFFFF",
            on_click=click,
        )
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
