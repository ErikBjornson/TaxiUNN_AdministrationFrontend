from .. import ft, Optional
from ..gui_elements import (
    HugeLabel,
    MessageLabel,
    InterfaceButton,
    InputField,
    GoBackButton,
)
from ..utils import (
    dp,
    list_tariff_req,
    SCREEN_SIZE,
)


class AddDriversPage:
    """Форма страницы для добавления новых водителей."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы добавления водителей."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.fields = {
            "name": InputField(
                top=180,
                left=462,
                text="Имя Фамилия",
                width=480,
                hint_text="Иван Иванов",
            ),
            "email": InputField(
                top=180,
                left=970,
                text="Почта",
                width=480,
            ),
            "brand": InputField(
                top=350,
                left=462,
                text="Марка автомобиля",
                width=480,
                hint_text="Lada",
            ),
            "model": InputField(
                top=350,
                left=970,
                text="Модель автомобиля",
                width=480,
                hint_text="Priora",
            ),
            "color": InputField(
                top=500,
                left=462,
                text="Цвет автомобиля",
                width=480,
                hint_text="Чёрный",
            ),
            "number": InputField(
                top=500,
                left=970,
                text="Государственный номер",
                width=480,
                hint_text="А111АА152",
            ),
        }

        self.tariffs_list = ft.Container(
            content=ft.Dropdown(
                width=dp(420),
                options=[
                    ft.dropdown.Option('Эконом'),
                    ft.dropdown.Option('Комфорт'),
                    ft.dropdown.Option('Комфорт+'),
                ],
                height=dp(80),
                hint_text="Тариф...",
                hint_style=ft.TextStyle(
                    font_family="Inter",
                    size=dp(26),
                ),
                padding=ft.padding.all(dp(5)),
                text_style=ft.TextStyle(
                    font_family="Inter",
                    size=dp(26),
                    color="#000000",
                ),
                bgcolor="#E8E8E8",
                icon_enabled_color="#4862E5",
                icon_disabled_color="#4862E5",
                border_radius=dp(22),
                border_color="#4862E5",
                border_width=dp(3),
            ),
            top=dp(660),
            left=dp(750),
            width=dp(420),
            height=dp(80),
        )

        self.error_label = MessageLabel(top=755)

    def clear_fields(self, action) -> None:
        """Метод очистки полей ввода и надписей."""
        for _, control in self.fields.items():
            control.clear()
        self.error_label.clear()
        self.page.update()

    async def add_driver(self, action) -> None:
        """Метод обработки события нажатия на кнопку 'Добавить'."""
        if not all((self.fields[key].get_value() for key in self.fields)):
            self.error_label.display_error("empty_fields")
            return

        await self.process_addding_driver()

    async def process_adding_driver(self) -> Optional[Exception]:
        """Метод отправки запроса на добавление водителя."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await list_tariff_req(token)

                if response.get('email'):
                    self.load_profile_info(response)
            else:
                raise ValueError('Значение токена невалидно.')

        except Exception as ex:
            return ex

    def to_profile(self, action) -> None:
        """Метод возвращения на страницу профиля."""
        self.clear_fields(action=None)
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
                                text="Добавление водителя",
                                top=80,
                            ),
                            self.tariffs_list,
                            self.error_label,
                            InterfaceButton(
                                text="Добавить",
                                top=820,
                                click=self.add_driver,
                                left=677,
                                width=265,
                            ),
                            InterfaceButton(
                                text="Очистить",
                                top=820,
                                click=self.clear_fields,
                                left=970,
                                width=265,
                                text_color="#1C1C1C",
                                bgcolor="#FFFFFF",
                            ),
                        ] + [self.fields[key] for key in self.fields],
                        width=SCREEN_SIZE[0],
                        height=SCREEN_SIZE[1],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self.page.title = "Добавление водителей"
        self.page.update()

        return self.page.controls, self.page.bgcolor
