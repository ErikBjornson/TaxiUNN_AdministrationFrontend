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

    "driver with this email already exists.":
        "Водитель с таким email уже зарегистрирован",

    "The verification code is not active.":
        "Неверный код верификации.",

    "User successfully registered.":
        "Новый пользователь успешно зарегистрирован",

    "Taxi fare with such name exist.":
        "Отредактируйте все тарифы с именем 'New tariff'",

    "empty_fields":
        "Все поля должны быть заполнены",

    "choose_tariff":
        "Выберите тариф водителя",

    "different_passwords":
        "Введённые пароли не совпадают",

    "to_short_passwords":
        "Пароль должен содержать не менее 8 символов",
}


def dp(value: int | None) -> float:
    """Функция для масштабирования элементов GUI."""
    return value if value is None else value / 1.5


def request(method: str):
    """
    Декоратор для запросов на сервер.

    При использовании необходимо указывать тип запроса
    на сервер (например, POST-запрос).
    """
    def request_decorator(func: callable):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            url, headers, payload = await func(*args, **kwargs)
            answer = None
            session = aiohttp.ClientSession()
            methods = {
                "POST": session.post,
                "GET": session.get,
                "PATCH": session.patch,
                "DELETE": session.delete,
            }

            async with session:

                request_method = methods.get(method)

                async with request_method(
                    url=url,
                    json=payload,
                    headers=headers,
                ) as response:
                    answer = await response.json()

            return answer

        return wrapper

    return request_decorator


def get_headers(access_token: str = None) -> dict[str, str]:
    """Функция создания заголовков для отправки запросов на сервер."""
    headers = {
        "Content-Type": "application/json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


@request(method="POST")
async def send_login_request(**kwargs):
    """
    Запрос на сервер - 'Авторизация администратора'.

    Если запрос успешный, происходит авторизация пользователя,
    в качестве ответа от сервера приходят access и refresh токены.
    Иначе приходит ответ о некорректно введённых данных.

    Аргументы:
        kwargs (dict[str, str]):

            1. email (str): логин (почтовый адрес) администратора,
            2. password (str): пароль от аккаунта администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (в данном случае только Content-Type),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/auth/login"
    return url, get_headers(), kwargs


@request(method="POST")
async def send_verification_code(**kwargs):
    """
    Запрос на сервер - 'Восстановление пароля администратора'.

    Если запрос успешный, сервер отправляет код верификации пользователя
    для восстановления (смены) пароля на указанный почтовый адрес,
    чтобы подтвердить, что именно этот пользователь собирается
    менять пароль.

    Аргументы:
        kwargs (dict[str, str]):

            1. email (str): логин (почтовый адрес) администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (в данном случае только Content-Type),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/auth/password-recovery"
    return url, get_headers(), kwargs


@request(method="POST")
async def do_verification(**kwargs):
    """
    Запрос на сервер - 'Верификация восстановления пароля администратора'.

    Данный запрос (если он успешный) отправляет код верификации
    восстановления (смены) пароля на указанный почтовый адрес.

    Аргументы:
        kwargs (dict[str, str]):

            1. email (str): логин (почтовый адрес) администратора,
            2. verification_code (str): код верификации пользователя.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (в данном случае только Content-Type),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/auth/password-recovery/verify"
    return url, get_headers(), kwargs


@request(method="POST")
async def change_password(**kwargs):
    """
    Запрос на сервер - 'Восстановление (смена) пароля администратора'.

    Если запрос успешный, у администратора изменяется пароль
    на новый введённый.

    Аргументы:
        kwargs (dict[str, str]):

            1. email (str): логин (почтовый адрес) администратора,
            2. password (str): новый пароль от аккаунта администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (в данном случае только Content-Type),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/auth/password-recovery/change"
    return url, get_headers(), kwargs


@request(method="GET")
async def load_profile_data(access_token: str):
    """
    Запрос на сервер - 'Получение данных профиля администратора'.

    Если запрос успешный, сервер в качестве ответа отправляет
    данные профиля пользователя (email - логин от аккаунта,
    full_name - полное имя администратора).

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access_token),
            3. Агрументы запроса (payload запроса - в данном случае None).
    """
    url = f"{BASE_URL}/admins"
    return url, get_headers(access_token), None


@request(method="POST")
async def register_new_admin(access_token: str, **kwargs):
    """
    Запрос на сервер - 'Регистрация нового администратора'.

    Если запрос успешный, сервер создаёт новый аккаунт администратора
    и присылает пароль от него на указанный почтовый адрес.

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        kwargs (dict[str, str]):

            1. email (str): почтовый адрес (логин) нового администратора,
            2. full_name (str): полное имя нового администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/auth/register"
    return url, get_headers(access_token), kwargs


@request(method="POST")
async def create_tariff_req(access_token: str, **kwargs):
    """
    Запрос на сервер - 'Создание нового тарифа'.

    Если запрос успешный, сервер в качестве ответа отправляет
    идентификатор нового тарифа в списке тарифов.

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        kwargs (dict[str, str]):

            1. name (str): название нового тарифа,
            2. price (int/float): почасовая стоимость нового тарифа.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/taxi_fare/"
    return url, get_headers(access_token), kwargs


@request(method="GET")
async def get_tariff_req(access_token: str, tariff_id: str):
    """
    Запрос на сервер - 'Получение конкретного тарифа по идентификатору'.

    Если запрос успешный, сервер в качестве ответа отправляет
    данные конкретного тарифа (название и почасовая стоимость тарифа).

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        tariff_id (str): идентификатор запрашиваемого тарифа.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса - в данном случае None).
    """
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    return url, get_headers(access_token), None


@request(method="PATCH")
async def patch_tariff_req(access_token: str, tariff_id: str, **kwargs):
    """
    Запрос на сервер - 'Изменение конкретного тарифа по идентификатору'.

    Если запрос успешный, сервер в качестве ответа отправляет
    сообщение, что тариф успешно изменён.

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        tariff_id (str): идентификатор запрашиваемого тарифа.

        kwargs (dict[str, str]):

            1. name (str): новое имя тарифа,
            2. price (int/float): новая почасовая стоимость тарифа.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    return url, get_headers(access_token), kwargs


@request(method="DELETE")
async def delete_tariff_req(access_token: str, tariff_id: str):
    """
    Запрос на сервер - 'Удаление конкретного тарифа по идентификатору'.

    Если запрос успешный, сервер в качестве ответа отправляет
    сообщение об успешном удалении тарифа из списка тарифов.

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        tariff_id (str): идентификатор запрашиваемого тарифа.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса - в данном случае None).
    """
    url = f"{BASE_URL}/taxi_fare/{tariff_id}/"
    return url, get_headers(access_token), None


@request(method="GET")
async def list_tariff_req(access_token: str):
    """
    Запрос на сервер - 'Получение полного списка существующих тарифов'.

    Если запрос успешный, сервер в качестве ответа отправляет
    список словарей - список тарифов с ключами id, name, price
    (идентификатор тарифа, название тарифа, почасовая стоимость).

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса - в данном случае None).
    """
    url = f"{BASE_URL}/taxi_fare/list/"
    return url, get_headers(access_token), None


@request(method="POST")
async def register_new_driver(access_token: str, **kwargs):
    """
    Запрос на сервер - 'Регистрация нового водителя'.

    Если запрос успешный, сервер создаёт новый аккаунт водителя
    и присылает пароль от него на указанный почтовый адрес.

    Аргументы:
        access_token (str): access-токен (токен доступа), полученный после
        авторизации администратора.

        kwargs (dict[str, str]):

            1. fare_id (str): идентификатор тарифа водителя в списке тарифов,
            2. email (str): почтовый адрес (логин) нового водителя,
            3. full_name (str): полное имя нового водителя,
            4. make (str): марка автомобиля водителя,
            5. model (str): модель автомобиля,
            6. color (str): цвет автомобиля,
            7. state_number (str): государственный номер автомобиля.

    Возвращаемое значение:
        tuple[ str, dict[str, str], dict[str, str] ]:

            1. URL-адрес, куда отправляется запрос,
            2. Заголовки для запроса (Authorization - Bearer access-token),
            3. Агрументы запроса (payload запроса).
    """
    url = f"{BASE_URL}/admins/driver-work/register"
    return url, get_headers(access_token), kwargs
