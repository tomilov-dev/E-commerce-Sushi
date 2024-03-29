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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget = forms.TextInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Номер телефона",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Пароль",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Повторите пароль",
            }
        )

        self.fields["phone"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("phone",)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-style text-field", "placeholder": "Номер телефона"}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-style text-field", "placeholder": "Пароль"}
        )


class RestorePasswordForm(forms.Form):
    phone = forms.CharField(
        max_length=12,
        label="Введите Ваш номер телефона",
        widget=forms.TextInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Номер телефона",
            }
        ),
    )
    password1 = forms.CharField(
        label="Введите новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Введите новый пароль",
            },
        ),
    )
    password2 = forms.CharField(
        label="Подтвердите новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Подтвердите новый пароль",
            },
        ),
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
    code = forms.CharField(
        max_length=6,
        label="Введите код подтверждения",
        widget=forms.TextInput(
            attrs={
                "class": "form-style text-field",
                "placeholder": "Код подтверждения",
            }
        ),
    )
