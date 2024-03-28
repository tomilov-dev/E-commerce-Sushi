import secrets
import hashlib
from datetime import datetime, timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .messages import LOGIN_LEVEL, RESEND_TEXT_LEVEL, RESEND_TIME_LEVEL
from .sms_sender import sms_sender
from .models import PhoneConfirmation, CustomUser
from .forms import (
    CustomUserCreationForm,
    PhoneConfirmationForm,
    CustomAuthenticationForm,
    RestorePasswordForm,
)


PHONE_HASH_SESSION_ID = settings.PHONE_HASH_SESSION_ID
RESEND_TIMER_SESSION_ID = settings.RESEND_TIMER_SESSION_ID
CODE_RESEND_TIME = 60


class Action(object):
    register = "register"
    restore = "restore"


def current_time() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def generate_code() -> str:
    return str(secrets.randbelow(10**6)).zfill(6)


def send_code(
    request: HttpRequest,
    phone: str,
    code: str,
) -> None:
    request.session[RESEND_TIMER_SESSION_ID] = CODE_RESEND_TIME
    sms_sender.send(phone, code)


def get_messages(request: HttpRequest, level: int) -> list:
    msg_list = messages.get_messages(request)
    msgs = [m.message for m in msg_list if m.level == level]
    return msgs


def save_phone_confirmation(
    phone: str,
    password: str,
    code: str,
) -> str:
    phone_hash = hashlib.sha256(phone.encode()).hexdigest()

    phoneExists = PhoneConfirmation.objects.filter(phone=phone).exists()
    if phoneExists:
        phone_confirmation = PhoneConfirmation.objects.get(phone=phone)
        phone_confirmation.code = code
        phone_confirmation.phone_hash = phone_hash
        phone_confirmation.password = password
        phone_confirmation.sent_time = current_time()
        phone_confirmation.save()

    else:
        PhoneConfirmation.objects.create(
            phone=phone,
            code=code,
            phone_hash=phone_hash,
            password=password,
            sent_time=current_time(),
        )

    return phone_hash


def resend_code(request: HttpRequest, action: Action) -> HttpResponse:
    phone_hash = request.session[PHONE_HASH_SESSION_ID]
    phone_confirmation = PhoneConfirmation.objects.get(
        phone_hash=phone_hash,
    )

    residue_time = CODE_RESEND_TIME - (current_time() - phone_confirmation.sent_time)
    if residue_time <= 0:
        phone = phone_confirmation.phone

        code = generate_code()
        phone_confirmation.code = code
        phone_confirmation.save()

        send_code(request, phone, code)
        return redirect("accounts:confirm_phone", action)

    else:
        messages.add_message(
            request,
            RESEND_TEXT_LEVEL,
            "Отправить новый код сейчас нельзя. Дождитесь установленного времени.",
        )
        messages.add_message(request, RESEND_TIME_LEVEL, residue_time)
        return redirect("accounts:confirm_phone", action)


def restore_password(request: HttpRequest) -> HttpResponse:
    errors = []
    if request.method == "POST":
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            code = generate_code()
            phone_hash = save_phone_confirmation(
                cleaned["phone"],
                cleaned["password2"],
                code,
            )

            request.session[PHONE_HASH_SESSION_ID] = phone_hash
            send_code(request, cleaned["phone"], code)
            return redirect("accounts:confirm_phone", Action.restore)

        else:
            errors = form.errors.values()

    return render(
        request,
        "accounts/restore_password.html",
        context={
            "restore_password_form": RestorePasswordForm(),
            "errors": errors,
        },
    )


def restore_user_password(phone: str, password: str) -> CustomUser:
    user = CustomUser.objects.get(
        phone=phone,
    )
    user.set_password(password)
    user.save()
    return user


def create_user(phone: str, password: str) -> CustomUser:
    return CustomUser.objects.create(
        phone=phone,
        password=password,
    )


def confirm_phone(request: HttpRequest, action: Action) -> HttpResponse:
    error_messages = []
    if request.method == "POST":
        form = PhoneConfirmationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            code = cleaned["code"]

            phone_hash = request.session.get(PHONE_HASH_SESSION_ID)
            if not phone_hash:
                raise Http404("Отсутствует хеш номера телефона! Повторите попытку. ")

            phone_confirmation = PhoneConfirmation.objects.get(phone_hash=phone_hash)
            if code == phone_confirmation.code:
                phone = phone_confirmation.phone
                password = phone_confirmation.password

                del request.session[PHONE_HASH_SESSION_ID]
                phone_confirmation.delete()

                if action == Action.restore:
                    user = restore_user_password(phone, password)
                    messages.add_message(request, LOGIN_LEVEL, "Пароль успешно сменен")
                    return redirect("accounts:account_login")

                elif action == Action.register:
                    user = create_user(phone, password)
                    login(request, user)
                    return redirect("pages:home")

                else:
                    raise Http404("Незарегистрированное действие")

            else:
                residue_time = CODE_RESEND_TIME - (
                    current_time() - phone_confirmation.sent_time
                )
                return render(
                    request,
                    "accounts/confirm_phone.html",
                    context={
                        "phone_confirmation_form": PhoneConfirmationForm(),
                        "errors": ["Введеный код не совпадает с отправленным"],
                        "resend_time": residue_time,
                        "action": action,
                    },
                )

        else:
            error_messages = form.errors.values()

    error_messages.extend(get_messages(request, RESEND_TEXT_LEVEL))
    residue_time = get_messages(request, RESEND_TIME_LEVEL)
    if residue_time:
        residue_time = int(residue_time[0])
    else:
        residue_time = CODE_RESEND_TIME

    return render(
        request,
        "accounts/confirm_phone.html",
        context={
            "phone_confirmation_form": PhoneConfirmationForm(),
            "resend_time": residue_time,
            "errors": error_messages,
            "action": action,
        },
    )


def account_register(request: HttpRequest) -> HttpResponse:
    errors = []
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            code = generate_code()
            phone_hash = save_phone_confirmation(
                cleaned["phone"],
                cleaned["password1"],
                code,
            )

            request.session[PHONE_HASH_SESSION_ID] = phone_hash
            send_code(request, cleaned["phone"], code)
            return redirect("accounts:confirm_phone", Action.register)

        else:
            errors = form.errors.values()

    return render(
        request,
        "accounts/register.html",
        context={
            "user_creation_form": CustomUserCreationForm(),
            "errors": errors,
        },
    )


def account_page(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        return render(
            request,
            "accounts/account.html",
            context={
                "user": user,
            },
        )

    else:
        return redirect("accounts:account_login")


def account_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            phone = cleaned["username"]
            password = cleaned["password"]
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect("pages:home")

        else:
            return render(
                request,
                "accounts/login.html",
                context={
                    "user_login_form": CustomAuthenticationForm(),
                    "errors": form.errors.values(),
                },
            )

    else:
        msgs = get_messages(request, LOGIN_LEVEL)
        return render(
            request,
            "accounts/login.html",
            context={
                "user_login_form": CustomAuthenticationForm(),
                "login_messages": msgs,
            },
        )


def account_logout(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        logout(request)
        return redirect("pages:home")
    else:
        return render(request, "accounts/logout.html")
