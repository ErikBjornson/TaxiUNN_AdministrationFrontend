from . import ft
from .gui_elements import (
    HugeLabel,
    InterfaceButton,
    GoBackButton,
    InterfaceLabel,
    InterfaceField,
)
from .utils import dp, SCREEN_SIZE


class TariffComponent(ft.Container):
    """Класс тарифа - компонента ft.ListView()."""

    def __init__(self) -> None:
        """Инициализация компонента."""
        super().__init__()
        self.tariff_data = {
            "name": "Новый тариф",
            "cost": "0",
        }
        self.buttons = {
            "edit": InterfaceButton(
                text="Редактировать",
                click=self.transform,
                top=None,
                left=None,
                width=210,
                height=55,
                text_size=20,
                text_color="#1C1C1C",
                bgcolor="#FFFFFF",
            ),
            "delete": InterfaceButton(
                text="Удалить",
                click=self.delete,
                top=None,
                left=None,
                width=145,
                height=55,
                text_size=20,
                text_color="#1C1C1C",
                bgcolor="#FFFFFF",
                border_color="#F44336",
            ),
            "save": InterfaceButton(
                text="Сохранить",
                click=self.save,
                top=None,
                left=None,
                width=210,
                height=55,
                text_size=20,
                text_color="#1C1C1C",
                bgcolor="#FFFFFF",
            ),
        }
        self.content = self.fget_content("simple")
        self.padding = ft.padding.all(dp(20))
        self.border_radius = dp(20)
        self.border = ft.border.all(
            width=dp(4),
            color="#E8E8E8",
        )
        self.width = dp(750)
        self.height = dp(180)

    def fget_content(self, option: str) -> ft.Row:
        """Метод получения актуального контента."""
        contents = {
            "simple":
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                InterfaceLabel(
                                    text=f"{self.tariff_data['name']}",
                                    size=35,
                                    width=300,
                                    height=48,
                                ),
                                InterfaceLabel(
                                    text=f"{self.tariff_data['cost']} руб/час",
                                    size=25,
                                    width=300,
                                    height=36,
                                ),
                            ],
                            width=dp(300),
                            height=dp(100),
                            alignment=ft.VerticalAlignment.CENTER,
                            horizontal_alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                self.buttons['edit'],
                                self.buttons['delete'],
                            ],
                            width=dp(380),
                            height=dp(55),
                            alignment=ft.VerticalAlignment.CENTER,
                        ),
                    ],
                    vertical_alignment=ft.VerticalAlignment.CENTER,
                ),
            "edit":
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                InterfaceField(
                                    width=300,
                                    height=60,
                                    hint_text="Тариф Эконом",
                                    field_id="tariff_name",
                                ),
                                InterfaceField(
                                    width=300,
                                    height=60,
                                    hint_text="Цена",
                                    suffix="руб/час",
                                    field_id="tariff_cost",
                                ),
                            ],
                            width=dp(300),
                            height=dp(150),
                            alignment=ft.VerticalAlignment.CENTER,
                            horizontal_alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                self.buttons['save'],
                                self.buttons['delete'],
                            ],
                            width=dp(380),
                            height=dp(55),
                            alignment=ft.VerticalAlignment.CENTER,
                        ),
                    ],
                    vertical_alignment=ft.VerticalAlignment.CENTER,
                ),
        }
        return contents[option]

    def transform(self, action) -> None:
        """Метод трансформации компонента для редактирования данных тарифа."""
        self.content = self.fget_content("edit")
        self.border = ft.border.all(
            width=dp(4),
            color="#000000",
        )
        self.page.update()

    def save(self, action) -> None:
        """Метод сохранения изменённых данных тарифа."""
        name = self.page.session.get('tariff_name')
        cost = self.page.session.get('tariff_cost')

        if not name or not cost:
            return

        self.tariff_data['name'] = name
        self.tariff_data['cost'] = cost

        self.page.session.remove('tariff_name')
        self.page.session.remove('tariff_cost')

        self.content = self.fget_content("simple")
        self.border = ft.border.all(
            width=dp(4),
            color="#E8E8E8",
        )
        self.page.update()

    def delete(self, action) -> None:
        """Метод удаления тарифа из списка."""


class TariffsList(ft.Container):
    """Класс прокручиваемого списка для отображения добавляемых тарифов."""

    def __init__(self) -> None:
        """Инициализация списка тарифов."""
        super().__init__()
        self.content = ft.ListView(
            controls=[],
            spacing=dp(10),
            width=dp(750),
            height=dp(500),
        )
        self.padding = ft.padding.all(dp(10))
        self.border_radius = dp(20)
        self.border = ft.border.all(
            width=dp(4),
            color="#E8E8E8",
        )
        self.top = dp(210)
        self.left = dp(580)

    def create_component(self) -> None:
        """Метод создания нового компонента и добавления его в список."""
        self.content.controls.append(TariffComponent())


class TariffsPage:
    """Форма страницы работы с тарифами для водителей и клиентов."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы работы с тарифами."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.tariffs_list = TariffsList()

    def clear_fields(self) -> None:
        """Метод очистки полей ввода и надписей."""

    def add_tariff(self, action) -> None:
        """Метод обработчик события нажатия на кнопку добавления тарифа."""
        self.tariffs_list.create_component()
        self.page.update()

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
                                text="Меню",
                                click=self.to_profile,
                            ),
                            HugeLabel(
                                text="Работа с тарифами",
                                top=110,
                            ),
                            self.tariffs_list,
                            InterfaceButton(
                                text="Добавить тариф",
                                top=780,
                                click=self.add_tariff,
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
        self.page.title = "Работа с тарифами"
        self.page.update()

        return self.page.controls, self.page.bgcolor
