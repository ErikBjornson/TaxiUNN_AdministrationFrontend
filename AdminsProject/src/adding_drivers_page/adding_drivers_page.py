from .. import ft, Optional
from ..gui_elements import (
    HugeLabel,
    MessageLabel,
    InterfaceButton,
    InputField,
    GoBackButton,
)
from ..utils import (
    register_new_driver,
    SCREEN_SIZE,
)
from .tariffs_dropdown_list import TariffsDropdownList
import asyncio


class AddDriversPage:
    """Форма страницы для добавления новых водителей."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы добавления водителей."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.fields = {
            "full_name": InputField(
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
            "make": InputField(
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
            "state_number": InputField(
                top=500,
                left=970,
                text="Государственный номер",
                width=480,
                hint_text="А111АА152",
            ),
        }

        self.tariffs_list = TariffsDropdownList()

        self.error_label = MessageLabel(top=755)

    async def add_driver(self, action) -> None:
        """Метод обработки события нажатия на кнопку 'Добавить'."""
        if not all((self.fields[key].get_value() for key in self.fields)):
            self.error_label.display_error("empty_fields")
            return

        if not self.tariffs_list.get_value():
            self.error_label.display_error("choose_tariff")
            return

        await self.process_adding_driver()

    async def process_adding_driver(self) -> Optional[Exception]:
        """Метод отправки запроса на добавление водителя."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await register_new_driver(
                    access_token=token,
                    fare_id=self.tariffs_list.get_value(),
                    full_name=self.fields.get('full_name').get_value(),
                    email=self.fields.get('email').get_value(),
                    make=self.fields.get('make').get_value(),
                    model=self.fields.get('model').get_value(),
                    color=self.fields.get('color').get_value(),
                    state_number=self.fields.get('state_number').get_value(),
                )

                if response.get('message'):
                    self.error_label.display_success(
                        response.get('message')[0],
                    )
                    self.clear_fields()

                else:
                    self.error_label.display_error(
                        response.get('email')[0],
                    )
            else:
                raise ValueError('Token not found.')

        except Exception as ex:
            return ex

    def clear_fields(self, action) -> None:
        """Метод очистки полей ввода и надписей."""
        for _, control in self.fields.items():
            control.clear()
        self.error_label.clear()
        self.page.update()

    def to_profile(self, action) -> None:
        """Метод возвращения на страницу профиля."""
        self.clear_fields(action=None)
        self.page.go("/profile")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        asyncio.create_task(self.tariffs_list.load_tariffs_list())
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            GoBackButton(
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
