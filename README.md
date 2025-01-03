# TaxiUNN - Фронтенд-часть сайта администрации сервиса заказа такси

![Static Badge](https://img.shields.io/badge/ErikBjornson-TaxiUNN_AdministrationFrontend-TaxiUNN_AdministrationFrontend)
![GitHub top language](https://img.shields.io/github/languages/top/ErikBjornson/TaxiUNN_AdministrationFrontend)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ErikBjornson/TaxiUNN_AdministrationFrontend)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/ErikBjornson/TaxiUNN_AdministrationFrontend)


## Обзор проекта

Фронтенд-часть административного сайта сервиса по заказу такси реализован на базе Python фреймворка Flet.

Бэкенд-часть всего сервиса реализована на базе Python фреймворка Django REST Framework.

Ссылка на бэкенд сервиса заказа такси: https://github.com/V-inTim/TaxiUNN

## Обзор страниц проекта

### Приветственная страница

![Welcome page overview](/images/welcomePage.png)

### Страница авторизации администратора

![Sign-in page overview](/images/signInPage.png)

### Страница восстановления пароля - ввод email

![Password recovery page overview](/images/passwordRecPage.png)

### Страница восстановления пароля - ввод кода верификации

![Password recovery verify page overview](/images/passwordRecVerifyPage.png)

### Страница восстановления пароля - смена пароля

![Password recovery setting new password page overview](/images/passwordRecNewPassPage.png)

### Страница профиля администратора

![Profile page overview](/images/profilePage.png)

### Страница работы (добавление/изменение/удаление) с тарифами

![Tariffs work page overview](/images/tariffsPage.png)

### Страница добавления новых водителей

![Adding new drivers page overview](/images/addingDriversPage.png)

### Страница добавления новых администраторов

![Adding new admins page overview](/images/addingAdminsPage.png)

## Что осталось не реализовано

1. Страница работы с клиентами (бэкенд не реализован, на фронтенде есть пустая страница-заглушка);
2. Страница работы с доходами (бэкенд не реализован, на фронтенде есть пустая страница-заглушка);
3. При удалении тарифа из списка тарифов отсутствует валидация того, что удаляемый тариф не назначен какому-либо водителю (если тариф назначен, то его удалять нельзя, однако возможно удалить его со страницы; при обновлении страницы удалённый тариф снова отобразится);
4. Отсутствуют куки-файлы для хранения access и refresh токенов (по-хорошему эти токены должны хранится в надёжном месте; в этом проекте токены хранятся в сессии страницы);
5. В поле ввода кода верификации при возвращении к предыдущей ячейке весь текст этой ячейки должен выделяться (во Flet отсутствуют методы выделения текста);
6. При переходе со страниц-опций (со страницы добавления администраторов или со страницы работы с тарифами) на страницу профиля, каждый раз отправляется запрос на сервер на получение данных профиля. Это некорректно и неэффективно. По-хорошему, эти данные нужно получать с сервера один раз после авторизации, сохранять в кэш и читать оттуда эти данные, а не отправлять запрос каждый раз;
7. Не реализована возможность просматривать списки добавленных администраторов и водителей.
