from src import ft


def main(page: ft.Page):
    """Главная функция запуска приложения."""


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="../AdminsProject/assets/",
)
