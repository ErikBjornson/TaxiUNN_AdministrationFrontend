from .. import ft
from ..utils import dp


class VerificationCodeInput(ft.Container):
    """Класс поля ввода кода верификации при восстановлении пароля."""

    def __init__(
        self,
        top: int = 470,
        left: int = 695,
        width: int = 530,
        height: int = 90,
    ) -> None:
        """Инициализация кастомного поля ввода."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height),
        )
        self.content = ft.Stack(
            controls=[
                ft.Column(
                    controls=[
                        ft.TextField(
                            width=dp(70),
                            height=dp(100),
                            border_color="#4862E5",
                            border_radius=dp(10),
                            border_width=dp(3),
                            bgcolor="#FFFFFF",
                            color="#000000",
                            multiline=False,
                            max_lines=1,
                            max_length=1,
                            counter_style=ft.TextStyle(
                                color="#FFFFFF",
                            ),
                            on_change=self.to_next,
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

    def fget_section(self, index: int) -> None:
        """Метод get для получения доступа к ячейке по индексу."""
        return self.array[index].controls[0]

    def get_code(self) -> str:
        """Метод get для вводимого кода - используется для валидации."""
        return self.values

    def to_next(self, action) -> None:
        """Метод перехода к следующей ячейке, если текущая уже заполнена."""
        if not self.fget_section(self.index).value:
            self.index = 0 if self.index == 0 else self.index - 1
            self.fget_section(self.index).focus()
            return

        self.values += self.fget_section(self.index).value

        if self.index < 4:
            self.fget_section(self.index + 1).focus()
            self.index += 1

    def clear_sections(self) -> None:
        """Метод очистки ячеек."""
        self.values = ""
        for index in range(5):
            self.fget_section(index).value = ""
        self.index = 0
        self.fget_section(self.index).focus()
