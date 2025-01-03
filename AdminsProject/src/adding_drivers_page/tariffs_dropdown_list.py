from .. import ft, Optional
from ..utils import dp, list_tariff_req


class TariffsDropdownList(ft.Container):
    """Класс выпадающего списка с тарифами."""

    def __init__(
        self,
        top: int = 660,
        left: int = 730,
        width: int = 460,
        height: int = 80,
    ) -> None:
        """Инициализация класса выпадающего списка."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height),
        )

        self.content = ft.Dropdown(
            width=dp(width),
            options=[],
            height=dp(height),
            max_menu_height=dp(height) * 2.5,
            hint_text="Тариф...",
            hint_style=ft.TextStyle(
                font_family="Inter",
                size=dp(24),
            ),
            padding=ft.padding.all(dp(5)),
            text_style=ft.TextStyle(
                font_family="Inter",
                size=dp(24),
                color="#000000",
            ),
            bgcolor="#E8E8E8",
            icon_enabled_color="#4862E5",
            icon_disabled_color="#4862E5",
            border_radius=dp(22),
            border_color="#4862E5",
            border_width=dp(3),
        )

    def get_value(self) -> str:
        """Метод get для получения идентификатора выбранного тарифа."""
        return self.content.value

    def set_options_list(self, tariffs: list) -> None:
        """Метод отображения списка списка тарифов."""
        self.content.options.clear()
        for item in tariffs:
            self.content.options.append(
                ft.dropdown.Option(
                    key=f"{item.get('id')}",
                    text=f"{item.get('name')} - {item.get('price')} руб/час",
                ),
            )
        self.page.update()

    async def load_tariffs_list(self) -> Optional[Exception]:
        """Метод отправки запроса на получение списка тарифов."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await list_tariff_req(access_token=token)

                if isinstance(response, list):
                    self.set_options_list(tariffs=response)

                else:
                    raise ValueError('Invalid access token.')

            else:
                raise ValueError('Token not found.')

        except Exception as ex:
            return ex
