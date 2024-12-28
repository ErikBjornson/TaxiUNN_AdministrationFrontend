import aiohttp
from functools import wraps

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


def request(method: str):
    """Декоратор для запросов на сервер."""
    def request_decorator(func: callable):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            url, headers, payload = await func(*args, **kwargs)
            answer = None

            async with aiohttp.ClientSession() as session:

                if method == "POST":
                    async with session.post(
                        url=url,
                        json=payload,
                        headers=headers,
                    ) as post_response:
                        answer = await post_response.json()

                elif method == "GET":
                    async with session.get(
                        url=url,
                        json=payload,
                        headers=headers,
                    ) as get_response:
                        answer = await get_response.json()

                elif method == "DELETE":
                    async with session.delete(
                        url=url,
                        json=payload,
                        headers=headers,
                    ) as delete_response:
                        answer = await delete_response.json()

                elif method == "PATCH":
                    async with session.patch(
                        url=url,
                        json=payload,
                        headers=headers,
                    ) as patch_response:
                        answer = await patch_response.json()

                return answer

        return wrapper

    return request_decorator


@request(method="POST")
async def send_login_request(email: str, password: str):
    """Функция для отправки данных для авторизации администратора."""
    url = f"{BASE_URL}/admins/auth/login"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "password": password,
    }
    return url, headers, payload


@request(method="POST")
async def send_verification_code(email: str):
    """Функция для отправки кода верификации - часть восстановления пароля."""
    url = f"{BASE_URL}/admins/auth/password-recovery"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
    }
    return url, headers, payload


@request(method="POST")
async def do_verification(email: str, verification_code: str):
    """Функция для проверки корректности введённого кода верификации."""
    url = f"{BASE_URL}/admins/auth/password-recovery/verify"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "verification_code": verification_code,
    }
    return url, headers, payload


@request(method="POST")
async def change_password(email: str, new_password: str):
    """Функция смены пароля администратора."""
    url = f"{BASE_URL}/admins/auth/password-recovery/change"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "password": new_password,
    }
    return url, headers, payload


@request(method="GET")
async def load_profile_data(access_token: str):
    """Функция получения данных профиля администратора."""
    url = f"{BASE_URL}/admins"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = None
    return url, headers, payload


@request(method="POST")
async def register_new_admin(access_token: str, email: str, full_name: str):
    """Функция регистрации нового администратора другим администратором."""
    url = f"{BASE_URL}/admins/auth/register"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "email": email,
        "full_name": full_name,
    }
    return url, headers, payload


@request(method="POST")
async def create_tariff_req(access_token: str, name: str, price: int):
    """Функция отправки запроса на создание тарифа."""
    url = f"{BASE_URL}/taxi_fare/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "name": name,
        "price": price,
    }
    return url, headers, payload


@request(method="GET")
async def get_tariff_req(access_token: str, tariff_id: str):
    """Функция отправки запроса на получение конкретного тарифа."""
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = None
    return url, headers, payload


@request(method="PATCH")
async def patch_tariff_req(
    access_token: str,
    tariff_id: str,
    name: str,
    price: str,
):
    """Функция отправки запроса на изменение тарифа."""
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "name": name,
        "price": price,
    }
    return url, headers, payload


@request(method="DELETE")
async def delete_tariff_req(access_token: str, tariff_id: str):
    """Функция отправки запроса на удаление тарифа."""
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = None
    return url, headers, payload


@request(method="GET")
async def list_tariff_req(access_token: str):
    """Функция отправки запроса на получение списка тарифов."""
    url = f"{BASE_URL}/taxi_fare/list/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = None
    return url, headers, payload


@request(method="POST")
async def driver_work(
    access_token: str,
    tariff_id: str,
    email: str,
    full_name: str,
    brand: str,
    model: str,
    color: str,
    number: str,
):
    """Функция отправки запроса на создание нового водителя."""
    url = f"{BASE_URL}/admins/drivers-work/register"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "fare_id": tariff_id,
        "email": email,
        "full_name": full_name,
        "make": brand,
        "model": model,
        "color": color,
        "state_number": number,
    }
    return url, headers, payload
