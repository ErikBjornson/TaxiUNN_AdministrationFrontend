from src import ft
from src import WelcomePage


def main(page: ft.Page):
    """Главная функция запуска приложения."""
    WelcomePage(page).display(action=None)
    page.update()


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="../AdminsProject/assets/",
)
