from . import ft, dp, SCREEN_SIZE


class WelcomePage:
    """Форма приветственной страницы."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация приветственной страницы."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.image = ft.Image(
            src="../assets/welcomePageImage.png",
            width=dp(1406),
            height=dp(1054),
            top=dp(-42),
            left=dp(-93),
            visible=True,
        )
        self.welcome_label = ft.Text(
            value="Добро пожаловать",
            size=dp(77),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(351) - dp(77) / 2,
            width=dp(473),
            height=dp(170) + dp(77) + dp(10),
            weight=dp(700),
            color="#1C1C1C",
            max_lines=2,
            visible=True,
        )
        self.annotation_label = ft.Text(
            value="Сервис для администрирования такси",
            size=dp(26),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(543),
            width=dp(501),
            height=dp(29) + dp(26),
            weight=dp(500),
            color="#A6A6A6",
            max_lines=1,
            visible=True,
        )
        self.enter_button = ft.ElevatedButton(
            text="Войти в аккаунт",
            width=dp(518),
            height=dp(84),
            top=dp(655),
            left=dp(0),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=dp(18)),
                padding=ft.Padding(
                    left=dp(80),
                    right=dp(80),
                    top=dp(20),
                    bottom=dp(20),
                ),
            ),
            bgcolor="#4862E5",
            color="#FFFFFF",
            visible=True,
            on_click=self.on_switch_to_sign_in,
        )

    def on_switch_to_sign_in(self, action) -> None:
        """Переход на экран авторизации - уход с приветственной страницы."""
        self.page.go("/login")

    def display(self, action) -> tuple[list[ft.Control], str]:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Stack(
                                controls=[
                                    self.image,
                                ],
                                width=SCREEN_SIZE[0] * 3 / 5,
                                height=SCREEN_SIZE[1],
                            ),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER,
                        horizontal_alignment=ft.ListTileTitleAlignment.TOP,
                    ),
                    ft.Column(
                        controls=[
                            ft.Stack(
                                controls=[
                                    self.welcome_label,
                                    self.annotation_label,
                                    self.enter_button,
                                ],
                                width=SCREEN_SIZE[0] * 2 / 5,
                                height=SCREEN_SIZE[1],
                            ),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER,
                        horizontal_alignment=ft.ListTileTitleAlignment.TOP,
                    ),
                ],
            ),
        )
        self.page.title = "Добро пожаловать!"
        self.page.update()

        return self.page.controls, self.page.bgcolor
