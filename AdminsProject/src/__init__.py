import flet as ft
from typing import Optional

from .welcome_page.welcome_page import WelcomePage
from .sign_in_page.sign_in_page import SignInPage
from .profile_page.profile_page import ProfilePage
from .clients_work_page.clients_work_page import ClientsWorkPage
from .income_work_page.income_work_page import IncomeWorkPage
from .tariffs_page.tariffs_page import TariffsPage
from .adding_drivers_page.adding_drivers_page import AddDriversPage
from .adding_admins_page.adding_admins_page import AddAdminsPage
from .password_recovery_pages.password_recovery_page import PasswordRecoveryPage
from .password_recovery_pages.password_recovery_verify_page import PasswordRecoveryVerifyPage
from .password_recovery_pages.password_recovery_change_pass_page import ChangePasswordPage

__all__ = [
    'ft',

    'WelcomePage',
    'SignInPage',
    'ProfilePage',
    'ClientsWorkPage',
    'IncomeWorkPage',
    'TariffsPage',
    'AddDriversPage',
    'AddAdminsPage',
    'PasswordRecoveryPage',
    'PasswordRecoveryVerifyPage',
    'ChangePasswordPage',

    'Optional',
]
