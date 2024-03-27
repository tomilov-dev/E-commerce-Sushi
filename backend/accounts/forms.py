from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("phone",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("phone",)


class CustomAuthenticationForm(AuthenticationForm):
    pass


class RestorePasswordForm(forms.Form):
    phone = forms.CharField(max_length=20, label="Введите Ваш номер телефона")
    password1 = forms.CharField(
        label="Введите новый пароль", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Подтвердите новый пароль", widget=forms.PasswordInput
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "Пользователь с указанным номером телефона не существует."
            )
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2


class PhoneConfirmationForm(forms.Form):
    code = forms.CharField(max_length=6, label="Введите код подтверждения")
