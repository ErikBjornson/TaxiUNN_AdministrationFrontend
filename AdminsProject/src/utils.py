import aiohttp

SCREEN_SIZE = 1250, 720

BASE_URL = "http://127.0.0.1:8000"

errors = {
    "Invalid credentials.":
        "Неверный пароль",

    "Enter a valid email address.":
        "Некорректный email",

    "An account with this email does not exist.":
        "Пользователь с таким email не существует",

    "empty_fields":
        "Все поля должны быть заполнены",

    "different_passwords":
        "Введённые пароли не совпадают",

    "to_short_passwords":
        "Пароль должен содержать не менее 8 символов",
}


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
            return await response.json()
