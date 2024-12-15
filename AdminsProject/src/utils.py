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

    "The verification code is not active.":
        "Неверный код верификации.",

    "empty_fields":
        "Все поля должны быть заполнены",

    "different_passwords":
        "Введённые пароли не совпадают",

    "to_short_passwords":
        "Пароль должен содержать не менее 8 символов",
}

hdrs = {
    "Content-Type": "application/json",
}


def dp(value: int) -> float:
    """Функция для масштабирования элементов GUI."""
    return value / 1.5


async def send_login_request(email, password):
    """Функция для отправки данных для авторизации администратора."""
    url = f"{BASE_URL}/admins/auth/login"
    payload = {
        "email": email,
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def send_verification_code(email):
    """Функция для отправки кода верификации - часть восстановления пароля."""
    url = f"{BASE_URL}/admins/auth/password-recovery"
    payload = {
        "email": email,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def do_verification(email, verification_code):
    """Функция для проверки корректности введённого кода верификации."""
    url = f"{BASE_URL}/admins/auth/password-recovery/verify"
    payload = {
        "email": email,
        "verification_code": verification_code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def change_password(email, new_password):
    """Функция смены пароля администратора."""
    url = f"{BASE_URL}/admins/auth/password-recovery/change"
    payload = {
        "email": email,
        "password": new_password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()
