from django.contrib.auth.base_user import BaseUserManager


def check_phone_number(phone: str) -> str:
    if phone.startswith("+7"):
        phone = phone[2:]
    elif phone.startswith("8"):
        phone = phone[1:]
    return phone


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("Для создания аккаунта необходимо указать номер телефона")

        phone = check_phone_number(phone)

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        phone = check_phone_number(phone)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Супер-пользователь должен иметь атрибут 'is_staff=True'")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Супер пользователь должен иметь атрибут 'is_superuser=True'"
            )
        return self.create_user(phone, password, **extra_fields)
