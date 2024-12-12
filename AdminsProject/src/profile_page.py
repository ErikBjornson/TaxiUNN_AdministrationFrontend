from . import ft, dp, SCREEN_SIZE


class Frame(ft.Container):
    """Вспомогательный класс - создаёт группу ft.Image() + ft.Text()."""

    def __init__(self, path: str, label: str, left: int) -> None:
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
        self.top = dp(501)
        self.left = dp(left)
        self.width = dp(246)
        self.height = dp(312)


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
        self.left = dp(879)
        self.width = dp(166)
        self.height = dp(166)


class ProfileInfo(ft.Container):
    """Класс, создающий поле 'Имя Фамилия' и поле с почтой."""

    def __init__(self, name: str, login: str) -> None:
        """Инициализация группы."""
        super().__init__()

        self.content = ft.Column(
            controls=[
                ft.Text(
                    value=f"{name}",
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
                    value=f"{login}",
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
        self.left = dp(762)
        self.width = dp(400)
        self.height = dp(90)


class ProfilePage:
    """Форма страницы профиля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы профиля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.switch_to_login_button = ft.ElevatedButton(
            text="Выйти",
            width=dp(200),
            height=dp(84),
            top=dp(80),
            left=dp(160),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=dp(40)),
            ),
            bgcolor="#4862E5",
            color="#FFFFFF",
            visible=True,
            on_click=self.to_login_page,
        )

    def to_login_page(self, action):
        """Метод logout - выход из аккунта и возврат к странице авторизации."""
        self.page.session.set("access_token", "")
        self.page.go("/login")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Stack(
                controls=[
                    self.switch_to_login_button,
                    ProfilePhoto(),
                    ProfileInfo(
                        name="Lion Alex",
                        login="test@gmail.com",
                    ),
                    Frame(
                        path="../assets/clientsWorkImage.png",
                        label="Работа с клиентами",
                        left=265,
                    ),
                    Frame(
                        path="../assets/incomeWorkImage.png",
                        label="Работа с доходами",
                        left=551,
                    ),
                    Frame(
                        path="../assets/tariffWorkImage.png",
                        label="Работа с тарифами",
                        left=837,
                    ),
                    Frame(
                        path="../assets/addingDriversImage.png",
                        label="Добавление\nводителей",
                        left=1123,
                    ),
                    Frame(
                        path="../assets/addingAdminsImage.png",
                        label="Добавление новых\nадминистраторов",
                        left=1409,
                    ),
                ],
                width=dp(SCREEN_SIZE[0]),
            ),
        )
        self.page.title = "Профиль"
        self.page.update()

        return self.page.controls, self.page.bgcolor
