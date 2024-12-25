import flet as ft
from typing import Optional

from .utils import (
    dp,
    send_login_request,
    send_verification_code,
    do_verification,
    change_password,
    SCREEN_SIZE,
    errors,
)

from .gui_elements import (
    HugeLabel,
    GrayLabel,
    MessageLabel,
    InputField,
    InterfaceButton,
    LinkButton,
    GoBackButton,
)
from .welcome_page import WelcomePage
from .sign_in_page import SignInPage
from .profile_page import ProfilePage
from .tariffs_page import TariffsPage
from .adding_admins_page import AddAdminsPage
from .password_recovery_page import PasswordRecoveryPage
from .password_recovery_verify_page import PasswordRecoveryVerifyPage
from .password_recovery_change_pass_page import ChangePasswordPage

__all__ = [
    'ft',
    'dp',
    'SCREEN_SIZE',
    'errors',

    'send_login_request',
    'send_verification_code',
    'do_verification',
    'change_password',

    'HugeLabel',
    'GrayLabel',
    'MessageLabel',
    'InputField',
    'InterfaceButton',
    'LinkButton',
    'GoBackButton',

    'WelcomePage',
    'SignInPage',
    'ProfilePage',
    'TariffsPage',
    'AddAdminsPage',
    'PasswordRecoveryPage',
    'PasswordRecoveryVerifyPage',
    'ChangePasswordPage',

    'Optional',
]
