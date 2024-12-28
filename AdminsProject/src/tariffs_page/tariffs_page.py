from .. import ft
from ..gui_elements import (
    HugeLabel,
    MessageLabel,
    InterfaceButton,
    GoBackButton,
)
from ..utils import (
    create_tariff_req,
    list_tariff_req,
    SCREEN_SIZE,
)
from .tariffs_list import tariffs_list
import asyncio


class TariffsPage:
    """Форма страницы работы с тарифами для водителей и клиентов."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы работы с тарифами."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.error_label = MessageLabel(
            top=770,
        )

    async def add_tariff(self, action) -> None:
        """Метод обработчик события нажатия на кнопку добавления тарифа."""
        await self.process_adding_tariff()

    async def process_adding_tariff(
        self,
        name: str = "New tariff",
        price: int = 1000,
    ):
        """Метод отправки запроса на добавление тарифа."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await create_tariff_req(
                    access_token=token,
                    name=name,
                    price=price,
                )

                if response.get('id'):
                    tariffs_list.create_component(
                        tariff_id=response.get('id'),
                    )
                    self.error_label.clear()

                elif response.get('name'):
                    self.error_label.display_error(
                        message=response.get('name')[0],
                    )

                else:
                    raise ValueError('Значение токена невалидно.')

            else:
                raise ValueError('Токен не найден.')

        except Exception as ex:
            return ex

    async def load_tariffs_list(self):
        """Метод загрузки списка тарифов с сервера."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await list_tariff_req(token)

                if isinstance(response, list):
                    for item in response:
                        tariffs_list.create_component(
                            tariff_id=item['id'],
                            name=item['name'],
                            price=item['price'],
                        )
                else:
                    raise ValueError('Значение токена невалидно.')

            else:
                raise ValueError('Токен не найден.')

        except Exception as ex:
            return ex

    def to_profile(self, action) -> None:
        """Метод возвращения на страницу профиля."""
        tariffs_list.clear_list()
        self.page.go("/profile")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        asyncio.create_task(self.load_tariffs_list())
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
                                top=80,
                            ),
                            tariffs_list,
                            self.error_label,
                            InterfaceButton(
                                text="Добавить тариф",
                                top=830,
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
