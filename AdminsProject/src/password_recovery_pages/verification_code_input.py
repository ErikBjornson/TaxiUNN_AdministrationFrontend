from .. import ft
from ..utils import dp


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
        if not self.get_value_of_section(self.index):
            self.to_previous(action=None)

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
