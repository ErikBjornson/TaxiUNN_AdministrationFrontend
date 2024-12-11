from . import ft, dp, SCREEN_SIZE


class PasswordRecoveryPage:
    """Форма страницы восстановления пароля администратора."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация страницы восстановления пароля."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"

        self.top_label = ft.Text(
            value="Восстановление\nпароля",
            size=dp(50),
            font_family="Inter",
            text_align=ft.TextAlign.CENTER,
            top=dp(194) - dp(50) / 2,
            left=dp(745),
            width=dp(429),
            height=dp(110) + dp(50) + dp(10),
            weight=dp(600),
            color="#1C1C1C",
            max_lines=2,
            visible=True,
        )

        self.email_label = ft.Text(
            value="Почта",
            size=dp(24),
            font_family="Inter",
            text_align=ft.TextAlign.LEFT,
            top=dp(354),
            left=dp(566) + dp(28) + dp(10),
            width=dp(732),
            height=dp(32),
            color="#1C1C1C",
        )

        self.email_field = ft.Container(
            content=ft.TextField(
                width=dp(732),
                height=dp(80),
                border_radius=dp(16),
                content_padding=dp(16),
                bgcolor="#E8E8E8",
                color="#000000",
                hint_style=ft.TextStyle(
                    size=dp(26),
                    font_family="Inter",
                    color="#6C6C6C",
                ),
                hint_text="Pochta@gmail.com",
                multiline=False,
                border_width=0,
            ),
            top=dp(354) + dp(32) + dp(10),
            left=dp(566) + dp(28),
            width=dp(732),
            height=dp(80),
        )

        self.send_code_button = ft.ElevatedButton(
            text="Отправить код",
            width=dp(420),
            height=dp(80),
            top=dp(806),
            left=dp(750),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=dp(18)),
                padding=ft.Padding(
                    left=dp(60),
                    right=dp(60),
                    top=dp(20),
                    bottom=dp(20),
                ),
            ),
            bgcolor="#4862E5",
            color="#FFFFFF",
            visible=True,
        )

    async def display(self, action) -> None:
        """Метод отображения формы на экране."""
        self.page.clean()
        self.page.add(
            ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            self.top_label,
                            self.email_label,
                            self.email_field,
                            self.send_code_button,
                        ],
                        width=dp(SCREEN_SIZE[0]),
                        height=dp(SCREEN_SIZE[1]),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self.page.title = "Восстановление пароля"
        self.page.update()