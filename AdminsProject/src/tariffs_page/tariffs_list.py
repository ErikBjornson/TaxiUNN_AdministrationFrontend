from .. import ft
from ..gui_elements import (
    InterfaceButton,
    InterfaceLabel,
    InterfaceField,
)
from ..utils import (
    dp,
    patch_tariff_req,
    delete_tariff_req,
)


class TariffComponent(ft.Container):
    """Класс тарифа - компонента ft.ListView()."""

    def __init__(
        self,
        tariff_id: int,
        name: str = "New tariff",
        price: int = 1000,
    ) -> None:
        """Инициализация компонента списка тарифов."""
        super().__init__()
        self.tariff_id = tariff_id
        self.tariff_data = {
            "name": name,
            "cost": price,
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
        """Метод получения актуального контента - внешнего вида компонента."""
        contents = {
            "simple": ft.Row(
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
            "edit": ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            InterfaceField(
                                width=300,
                                height=60,
                                size=26,
                                hint_text="Тариф Эконом",
                                field_id="tariff_name",
                            ),
                            InterfaceField(
                                width=300,
                                height=60,
                                size=26,
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

    async def save(self, action) -> None:
        """Метод сохранения изменённых данных тарифа."""
        name = self.page.session.get('tariff_name')
        cost = self.page.session.get('tariff_cost')

        if not name or not cost:
            return

        self.tariff_data['name'] = name
        self.tariff_data['cost'] = cost

        self.page.session.remove('tariff_name')
        self.page.session.remove('tariff_cost')

        await self.change_tariff()

        self.content = self.fget_content("simple")
        self.border = ft.border.all(
            width=dp(4),
            color="#E8E8E8",
        )
        self.page.update()

    async def change_tariff(self):
        """Отправка запроса на изменение тарифа (редактирование)."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await patch_tariff_req(
                    access_token=token,
                    tariff_id=self.tariff_id,
                    name=self.tariff_data['name'],
                    price=int(self.tariff_data['cost']),
                )

                if response.get('message'):
                    raise ValueError('Некорректные данные.')

            else:
                raise ValueError('Значение токена невалидно.')

        except Exception as ex:
            return ex

    async def delete(self, action) -> None:
        """Метод удаления тарифа из списка."""
        await self.remove_tariff()
        tariffs_list.delete_component(self)

    async def remove_tariff(self):
        """Отправка запроса на удаление тарифа."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await delete_tariff_req(token, self.tariff_id)

                if response.get('message'):
                    raise ValueError('Неверное значение идентификатора.')

            else:
                raise ValueError('Значение токена невалидно.')

        except Exception as ex:
            return ex


class TariffsList(ft.Container):
    """Класс прокручиваемого списка для отображения добавляемых тарифов."""

    def __init__(
        self,
        top: int = 160,
        left: int = 580,
    ) -> None:
        """Инициализация списка тарифов."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            padding=ft.padding.all(dp(10)),
            border_radius=dp(20),
            border=ft.border.all(
                width=dp(4),
                color="#E8E8E8",
            ),
        )

        self.content = ft.ListView(
            controls=[],
            on_scroll_interval=50,
            spacing=dp(10),
            width=dp(750),
            height=dp(560),
        )

    def create_component(
        self,
        tariff_id: int,
        name: str = "New tariff",
        price: int = 1000,
    ) -> None:
        """Метод создания нового компонента и добавления его в список."""
        self.content.controls.append(
            TariffComponent(
                tariff_id=tariff_id,
                name=name,
                price=price,
            ),
        )
        self.page.update()

    def delete_component(self, component) -> None:
        """Метод удаления компонента из списка."""
        self.content.controls.remove(component)
        self.page.update()

    def clear_list(self) -> None:
        """Метод полной очистки списка тарифов."""
        self.content.controls.clear()
        self.page.update()


tariffs_list = TariffsList()
