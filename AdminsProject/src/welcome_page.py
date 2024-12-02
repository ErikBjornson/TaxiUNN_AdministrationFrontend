from . import ft, dp, SCREEN_SIZE


class WelcomePage:
    """Форма приветственной страницы."""

    def __init__(self, page: ft.Page):
        """Инициализация приветственной страницы."""
        self.page = page
        self.page.title = "Добро пожаловать!"
        self.page.bgcolor = "#FFFFFF"

        self.image = ft.Image(
            src="../assets/welcomePageImage.png",
            width=dp(1406),
            height=dp(1054),
            top=dp(22),
            left=dp(-93),
            visible=True,
        )
        self.welcome_label = ft.Text(
            value="Добро пожаловать",
            size=dp(77),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(361) - dp(77) / 2,
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
            top=dp(553),
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
            top=dp(665),
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
        )

    def display(self, action) -> None:
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
                                width=dp(SCREEN_SIZE[0]) * 3 / 5,
                                height=dp(SCREEN_SIZE[1]),
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
                                width=dp(SCREEN_SIZE[0]) * 2 / 5,
                                height=dp(SCREEN_SIZE[1]),
                            ),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER,
                        horizontal_alignment=ft.ListTileTitleAlignment.TOP,
                    ),
                ],
            ),
        )
