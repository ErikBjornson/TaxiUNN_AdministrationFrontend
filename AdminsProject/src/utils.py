import aiohttp

BASE_URL = "http://127.0.0.1:8000"

SCREEN_SIZE = 1250, 720

errors = {
    "Invalid credentials.":
        "Неверный пароль",

    "Enter a valid email address.":
        "Некорректный email",

    "An account with this email does not exist.":
        "Пользователь с таким email не существует",

    "An account with this email exist.":
        "Пользователь с таким email уже существует",

    "The verification code is not active.":
        "Неверный код верификации.",

    "User successfully registered.":
        "Новый администратор успешно зарегистрирован",

    "empty_fields":
        "Все поля должны быть заполнены",

    "different_passwords":
        "Введённые пароли не совпадают",

    "to_short_passwords":
        "Пароль должен содержать не менее 8 символов",
}


def dp(value: int | None) -> float:
    """Функция для масштабирования элементов GUI."""
    if value is None:
        return value
    return value / 1.5


hdrs = {
    "Content-Type": "application/json",
}


async def send_login_request(email: str, password: str):
    """Функция для отправки данных для авторизации администратора."""
    url = f"{BASE_URL}/admins/auth/login"
    payload = {
        "email": email,
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def send_verification_code(email: str):
    """Функция для отправки кода верификации - часть восстановления пароля."""
    url = f"{BASE_URL}/admins/auth/password-recovery"
    payload = {
        "email": email,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def do_verification(email: str, verification_code: str):
    """Функция для проверки корректности введённого кода верификации."""
    url = f"{BASE_URL}/admins/auth/password-recovery/verify"
    payload = {
        "email": email,
        "verification_code": verification_code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def change_password(email: str, new_password: str):
    """Функция смены пароля администратора."""
    url = f"{BASE_URL}/admins/auth/password-recovery/change"
    payload = {
        "email": email,
        "password": new_password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=hdrs) as response:
            return await response.json()


async def load_profile_data(access_token: str):
    """Функция получения данных профиля администратора."""
    url = f"{BASE_URL}/admins"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def register_new_admin(access_token: str, email: str, full_name: str):
    """Функция регистрации нового администратора другим администратором."""
    url = f"{BASE_URL}/admins/auth/register"
    head = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "email": email,
        "full_name": full_name,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=head) as response:
            return await response.json()
