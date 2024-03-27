import secrets
import hashlib
from datetime import datetime, timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.contrib import messages

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


LOGIN_LEVEL = 66
RESEND_TEXT_LEVEL = 67
RESEND_TIME_LEVEL = 68


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


def resend_code(request: HttpRequest) -> HttpResponse:
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
        return redirect("accounts:confirm_phone")

    else:
        messages.add_message(
            request,
            RESEND_TEXT_LEVEL,
            "Отправить новый код сейчас нельзя. Дождитесь установленного времени.",
        )
        messages.add_message(request, RESEND_TIME_LEVEL, residue_time)
        return redirect("accounts:confirm_phone")


def resend_restore_code(request: HttpRequest) -> HttpResponse:
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
        return redirect("accounts:restore_confirm")

    else:
        messages.add_message(
            request,
            RESEND_TEXT_LEVEL,
            "Отправить новый код сейчас нельзя. Дождитесь установленного времени.",
        )
        messages.add_message(request, RESEND_TIME_LEVEL, residue_time)
        return redirect("accounts:restore_confirm")


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


def restore_password(request: HttpRequest) -> HttpResponse:
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
            return redirect("accounts:restore_confirm")

    else:
        return render(
            request,
            "accounts/restore_password.html",
            context={
                "restore_password_form": RestorePasswordForm(),
            },
        )


def restore_password_confim(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PhoneConfirmationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            code = cleaned["code"]

            phone_hash = request.session.get(PHONE_HASH_SESSION_ID)
            if not phone_hash:
                raise Http404("Отсутствует хеш номера телефона!")

            phone_confirmation = PhoneConfirmation.objects.get(phone_hash=phone_hash)
            if code == phone_confirmation.code:
                user = CustomUser.objects.get(
                    phone=phone_confirmation.phone,
                )
                user.set_password(phone_confirmation.password)
                user.save()

                del request.session[PHONE_HASH_SESSION_ID]
                phone_confirmation.delete()

                messages.add_message(
                    request,
                    LOGIN_LEVEL,
                    "Пароль успешно сменен",
                )
                return redirect("accounts:account_login")

            else:
                residue_time = CODE_RESEND_TIME - (
                    current_time() - phone_confirmation.sent_time
                )
                return render(
                    request,
                    "accounts/restore_confirm_phone.html",
                    context={
                        "phone_confirmation_form": PhoneConfirmationForm(),
                        "resend_time": residue_time,
                        "errors": ["Введеный код не совпадает с отправленным"],
                    },
                )

    else:
        messages_list = messages.get_messages(request)

        residue_time = None
        error_messages = []
        for message in messages_list:
            if message.level == RESEND_TIME_LEVEL:
                try:
                    residue_time = int(message.message)
                except:
                    pass
            elif message.level == RESEND_TEXT_LEVEL:
                error_messages.append(message.message)

        if not residue_time:
            residue_time = CODE_RESEND_TIME

        return render(
            request,
            "accounts/restore_confirm_phone.html",
            context={
                "phone_confirmation_form": PhoneConfirmationForm(),
                "resend_time": residue_time,
                "errors": error_messages,
            },
        )


def confirm_phone(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PhoneConfirmationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            code = cleaned["code"]

            phone_hash = request.session.get(PHONE_HASH_SESSION_ID)
            if not phone_hash:
                raise Http404("Отсутствует хеш номера телефона!")

            phone_confirmation = PhoneConfirmation.objects.get(phone_hash=phone_hash)
            if code == phone_confirmation.code:
                user = CustomUser.objects.create(
                    phone=phone_confirmation.phone,
                    password=phone_confirmation.password,
                )

                del request.session[PHONE_HASH_SESSION_ID]
                phone_confirmation.delete()

                login(request, user)
                return redirect("pages:home")

            else:
                residue_time = CODE_RESEND_TIME - (
                    current_time() - phone_confirmation.sent_time
                )
                return render(
                    request,
                    "accounts/confirm_phone.html",
                    context={
                        "phone_confirmation_form": PhoneConfirmationForm(),
                        "resend_time": residue_time,
                        "errors": ["Введеный код не совпадает с отправленным"],
                    },
                )

        else:
            raise Http404("Ошибка при валидации формы!")

    else:
        messages_list = messages.get_messages(request)

        residue_time = None
        error_messages = []
        for message in messages_list:
            if message.level == RESEND_TIME_LEVEL:
                try:
                    residue_time = int(message.message)
                except:
                    pass
            elif message.level == RESEND_TEXT_LEVEL:
                error_messages.append(message.message)

        if not residue_time:
            residue_time = CODE_RESEND_TIME

        return render(
            request,
            "accounts/confirm_phone.html",
            context={
                "phone_confirmation_form": PhoneConfirmationForm(),
                "resend_time": residue_time,
                "errors": error_messages,
            },
        )


def account_register(request: HttpRequest) -> HttpResponse:
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
            return redirect("accounts:confirm_phone")

        else:
            return render(
                request,
                "accounts/register.html",
                context={
                    "user_creation_form": CustomUserCreationForm(),
                    "errors": form.errors.values(),
                },
            )

    else:
        return render(
            request,
            "accounts/register.html",
            context={
                "user_creation_form": CustomUserCreationForm(),
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
        msg_list = messages.get_messages(request)
        msgs = [m.message for m in msg_list if m.level == LOGIN_LEVEL]

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
