import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs) -> None:
        if not User.objects.filter(is_superuser=True).exists():
            phone = os.getenv("DJANGO_SUPERUSER_USERNAME")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

            User.objects.create_superuser(
                phone=phone,
                email="",
                password=password,
            )
