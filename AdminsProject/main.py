from src import (
    ft,
    WelcomePage,
    SignInPage,
    ProfilePage,
    PasswordRecoveryPage,
)


class MainFrame:
    """Главный класс, управляющий навигацией между страницами."""

    def __init__(self, page: ft.Page) -> None:
        """Инициализация класса навигации - создание страниц."""
        self.page = page
        self.page.bgcolor = "#FFFFFF"
        self.pages = {
            "/": WelcomePage(page),
            "/login": SignInPage(page),
            "/profile": ProfilePage(page),
            "/password-recovery": PasswordRecoveryPage(page),
        }
        self.page.on_route_change = self.change_route
        self.page.go(self.page.route)

    async def change_route(self, action) -> None:
        """Метод обновляет содержимое страницы в зависимости от маршрута."""
        self.page.views.clear()
        controls, color = self.pages[self.page.route].display(action=None)
        self.page.views.append(
            ft.View(
                route="/",
                controls=controls,
                bgcolor=color,
            ),
        )
        self.page.update()


async def main(page: ft.Page):
    """Главная функция запуска приложения."""
    MainFrame(page)
    page.update()


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="../AdminsProject/assets/",
)
