import os
import requests
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from django.conf import settings


load_dotenv()
check_env = os.getenv("ENV_CHECK")
if not check_env:
    raise FileNotFoundError(".env file not found")

DEBUG = settings.DEBUG

SMSAERO_APIKEY = os.getenv("SMSAERO_APIKEY")
SMSAERO_EMAIL = os.getenv("SMSAERO_EMAIL")


class SMSSender(ABC):
    @abstractmethod
    def send(self, phone: str, code: str) -> None:
        pass


class ConsoleSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        print(phone, code)


class SMSAeroSender(SMSSender):
    def __init__(self, email: str, apikey: str) -> None:
        self.email = email
        self.apikey = apikey

    def send(self, phone: str, code: str) -> None:
        response = requests.post(
            f"https://{self.email}:{self.apikey}@gate.smsaero.ru/v2/sms/send",
            {
                "number": phone,
                "sign": "SMS Aero",
                "text": f"Служба доставки Tomilov-Delivery.\nВаш код регистрации: {code}",
            },
        )

        # print(response)
        # print(response.text)


if DEBUG:
    sms_sender = ConsoleSender()
else:
    sms_sender = SMSAeroSender(SMSAERO_EMAIL, SMSAERO_APIKEY)
