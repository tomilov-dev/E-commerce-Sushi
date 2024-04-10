from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from .managers import check_phone_number


class CustomPhoneAuthBackend(BaseBackend):
    def authenticate(
        self,
        request,
        phone=None,
        password=None,
        **kwargs,
    ):
        UserModel = get_user_model()

        if not phone:
            phone = kwargs.get("username")
        phone = check_phone_number(phone)

        try:
            user = UserModel.objects.get(phone=phone)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and user.phone == phone:
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
