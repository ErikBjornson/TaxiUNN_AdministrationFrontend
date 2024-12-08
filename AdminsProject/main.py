from src import (
    ft,
    WelcomePage,
    SignInPage,
    ProfilePage,
)


async def main(page: ft.Page):
    """Главная функция запуска приложения."""
    profile = ProfilePage(page=page)

    async def on_success(action) -> None:
        """Переход на экран профиля - авторизация прошла успешно."""
        await profile.display(action=action)

    sign_in = SignInPage(
        page=page,
        on_success=on_success,
    )

    async def on_switch_to_sign_in(action) -> None:
        """Переход на экран авторизации - уход с приветственной страницы."""
        await sign_in.display(action=action)

    welcome = WelcomePage(
        page=page,
        on_switch_to_sign_in=on_switch_to_sign_in,
    )

    await welcome.display(action=None)


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="../AdminsProject/assets/",
)
