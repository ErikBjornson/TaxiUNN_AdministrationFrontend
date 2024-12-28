from .. import ft, Optional
from ..gui_elements import GoBackButton
from ..utils import load_profile_data, SCREEN_SIZE

from .option_frame import Frame
from .profile_info import ProfileInfo
from .profile_photo import ProfilePhoto

import asyncio


class ProfilePage:
    """Форма страницы профиля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы профиля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.options = {
            "client_work": Frame(
                image_path="../assets/clientsWorkImage.png",
                text="Работа с клиентами",
                left=240,
            ),

            "income_work": Frame(
                image_path="../assets/incomeWorkImage.png",
                text="Работа с доходами",
                left=526,
            ),

            "tariffs_work": Frame(
                image_path="../assets/tariffWorkImage.png",
                text="Работа с тарифами",
                left=812,
                route="/profile/tariffs",
            ),

            "adding_drivers": Frame(
                image_path="../assets/addingDriversImage.png",
                text="Добавление\nводителей",
                left=1098,
                route="/profile/add-drivers",
            ),

            "adding_admins": Frame(
                image_path="../assets/addingAdminsImage.png",
                text="Добавление новых\nадминистраторов",
                left=1384,
                route="/profile/add-admins",
            ),
        }

        self.profile_info = ProfileInfo()

    async def load_user_data(self) -> Optional[Exception]:
        """Получения данных пользователя с сервера."""
        try:
            token = self.page.session.get('access_token')

            if token:
                response = await load_profile_data(token)

                if response.get('email'):
                    self.load_profile_info(response)
            else:
                raise ValueError('Значение токена невалидно.')

        except Exception as ex:
            return ex

    def load_profile_info(self, data):
        """Обновление надписей данных профиля."""
        self.profile_info.update_profile_info(
            name=data.get('full_name'),
            login=data.get('email'),
        )

    def to_login(self, action) -> None:
        """Метод logout - выход из аккунта и возврат к странице авторизации."""
        self.page.session.remove("access_token")
        self.page.go("/login")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        asyncio.create_task(self.load_user_data())  # загрузка данных профиля
        self.page.add(
            ft.Stack(
                controls=[
                    GoBackButton(
                        text="Выйти",
                        click=self.to_login,
                    ),
                    ProfilePhoto(),
                    self.profile_info,
                ] + [self.options[key] for key in self.options],
                width=SCREEN_SIZE[0],
            ),
        )
        self.page.title = "Профиль"
        self.page.update()

        return self.page.controls, self.page.bgcolor
