from . import ft, Optional
from .gui_elements import GoBackButton
from .utils import dp, load_profile_data, SCREEN_SIZE
import asyncio


class ProfilePhoto(ft.Container):
    """Класс, создающий место для фотографии профиля."""

    def __init__(self) -> None:
        """Инициализация объекта."""
        super().__init__()

        self.content = ft.IconButton(
            icon=ft.icons.PHOTO_CAMERA_OUTLINED,
            width=dp(166),
            height=dp(166),
            icon_color="#A6A6A6",
            icon_size=dp(65),
            style=ft.ButtonStyle(
                bgcolor="#D0D0D0",
            ),
        )
        self.top = dp(110)
        self.left = dp(854)
        self.width = dp(166)
        self.height = dp(166)


class ProfileInfo(ft.Container):
    """Класс, создающий поле 'Имя Фамилия' и поле с почтой."""

    def __init__(self) -> None:
        """Инициализация группы."""
        super().__init__()

        self.content = ft.Column(
            controls=[
                ft.Text(
                    value=" ",
                    size=dp(40),
                    font_family="Inter",
                    text_align=ft.TextAlign.CENTER,
                    width=dp(400),
                    height=dp(50),
                    weight=dp(600),
                    color="#1C1C1C",
                    max_lines=1,
                    visible=True,
                ),
                ft.Text(
                    value=" ",
                    size=dp(24),
                    font_family="Inter",
                    text_align=ft.TextAlign.CENTER,
                    width=dp(400),
                    height=dp(35),
                    weight=dp(400),
                    color="#A0A0A0",
                    max_lines=1,
                    visible=True,
                ),
            ],
        )
        self.top = dp(296)
        self.left = dp(737)
        self.width = dp(400)
        self.height = dp(90)

    def update_profile_info(self, name: str, login: str) -> None:
        """Заполнение данных профиля."""
        self.content.controls[0].value = name
        self.content.controls[1].value = login
        self.page.update()


class Frame(ft.Container):
    """Вспомогательный класс - создаёт группу ft.Image() + ft.Text()."""

    def __init__(self, path: str, label: str, left: int, click=None) -> None:
        """Инициализация группы."""
        super().__init__()

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=path,
                        width=dp(246),
                        height=dp(246),
                        border_radius=ft.border_radius.all(dp(18)),
                        visible=True,
                    ),
                    border=ft.border.all(dp(3)),
                    border_radius=ft.border_radius.all(dp(18)),
                    width=dp(246),
                    height=dp(246),
                    on_click=click,
                ),
                ft.Text(
                    value=label,
                    size=dp(20),
                    font_family="Inter",
                    text_align=ft.TextAlign.CENTER,
                    width=dp(246),
                    height=dp(48) + dp(20),
                    weight=dp(500),
                    color="#1C1C1C",
                    max_lines=2,
                    visible=True,
                ),
            ],
        )
        self.top = dp(581)
        self.left = dp(left)
        self.width = dp(246)
        self.height = dp(312)


class ProfilePage:
    """Форма страницы профиля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы профиля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.clients_work = Frame(
            path="../assets/clientsWorkImage.png",
            label="Работа с клиентами",
            left=240,
        )

        self.income_work = Frame(
            path="../assets/incomeWorkImage.png",
            label="Работа с доходами",
            left=526,
        )

        self.tariffs_work = Frame(
            path="../assets/tariffWorkImage.png",
            label="Работа с тарифами",
            left=812,
            click=self.to_tariffs,
        )

        self.adding_drivers = Frame(
            path="../assets/addingDriversImage.png",
            label="Добавление\nводителей",
            left=1098,
            click=self.to_add_drivers,
        )

        self.adding_admins = Frame(
            path="../assets/addingAdminsImage.png",
            label="Добавление новых\nадминистраторов",
            left=1384,
            click=self.to_add_admins,
        )
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

    def to_tariffs(self, action) -> None:
        """Метод перехода на страницу добавления тарифов."""
        self.page.go("/profile/tariffs")

    def to_add_drivers(self, action) -> None:
        """Мктод перехода на страницу добавления новых водителей."""
        self.page.go("/profile/add-drivers")

    def to_add_admins(self, action) -> None:
        """Метод перехода на страницу добавления новых администраторов."""
        self.page.go("/profile/add-admins")

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
                    self.clients_work,
                    self.income_work,
                    self.tariffs_work,
                    self.adding_drivers,
                    self.adding_admins,
                ],
                width=SCREEN_SIZE[0],
            ),
        )
        self.page.title = "Профиль"
        self.page.update()

        return self.page.controls, self.page.bgcolor
