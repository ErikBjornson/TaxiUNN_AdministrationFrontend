from .. import ft
from ..utils import dp


class ProfilePhoto(ft.Container):
    """Класс, создающий место для фотографии профиля."""

    def __init__(
        self,
        top: int = 110,
        left: int = 854,
        width: int = 166,
        height: int = 166,
    ) -> None:
        """Инициализация объекта."""
        super().__init__(
            top=dp(top),
            left=dp(left),
            width=dp(width),
            height=dp(height),
        )

        self.content = ft.IconButton(
            icon=ft.icons.PHOTO_CAMERA_OUTLINED,
            width=dp(width),
            height=dp(width),
            icon_color="#A6A6A6",
            icon_size=dp(65),
            style=ft.ButtonStyle(
                bgcolor="#D0D0D0",
            ),
        )
