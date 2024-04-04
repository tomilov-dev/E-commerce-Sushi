from django.urls import path

from .views import (
    account_register,
    confirm_phone,
    account_login,
    account_page,
    account_logout,
    resend_code,
    restore_password,
    change_password,
    change_phone,
    change_presonal_info,
)

app_name = "accounts"

urlpatterns = [
    path("", account_page, name="account_page"),
    path("logout/", account_logout, name="account_logout"),
    path("login/", account_login, name="account_login"),
    path("register/", account_register, name="account_register"),
    path("confirm/<str:action>/", confirm_phone, name="confirm_phone"),
    path("resend/<str:action>", resend_code, name="resend_code"),
    path("restore_password/", restore_password, name="restore_password"),
    path("change_password/", change_password, name="change_password"),
    path("change_phone/", change_phone, name="change_phone"),
    path("change_presonal_info/", change_presonal_info, name="change_presonal_info"),
]
