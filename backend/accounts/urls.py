from django.urls import path

from .views import (
    account_register,
    confirm_phone,
    account_login,
    account_page,
    account_logout,
    resend_code,
    restore_password,
    restore_password_confim,
    resend_restore_code,
)

app_name = "accounts"

urlpatterns = [
    path("", account_page, name="account_page"),
    path("logout/", account_logout, name="account_logout"),
    path("login/", account_login, name="account_login"),
    path("register/", account_register, name="account_register"),
    path("confirm/", confirm_phone, name="confirm_phone"),
    path("resend/", resend_code, name="resend_code"),
    path("restore_password/", restore_password, name="restore_password"),
    path("restore_confirm/", restore_password_confim, name="restore_confirm"),
    path("resend_restore_code/", resend_restore_code, name="resend_restore_code"),
]
