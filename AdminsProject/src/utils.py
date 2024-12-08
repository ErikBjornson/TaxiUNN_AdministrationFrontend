import aiohttp

SCREEN_SIZE = 1920, 1080

BASE_URL = "http://127.0.0.1:8000"


def dp(value: int) -> float:
    """Функция для масштабирования элементов GUI."""
    return value / 1.5


async def send_login_request(email, password):
    """Метод для авторизации пользователя."""
    url = f"{BASE_URL}/admins/auth/login"
    hdrs = {
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            if response.status == 200:
                return await response.json()
            error_message = await response.text()
            raise ConnectionError(
                f"Ошибка входа: {error_message}",
            )
