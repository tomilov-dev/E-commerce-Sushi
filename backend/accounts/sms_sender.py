import os
import requests
from dotenv import load_dotenv
from abc import ABC, abstractmethod


load_dotenv()
check_env = os.getenv("ENV_CHECK")
if not check_env:
    raise FileNotFoundError(".env file not found")

SMSAERO_APIKEY = os.getenv("ENV_CHECK")
SMSAERO_EMAIL = os.getenv("ENV_CHECK")
DEBUG = os.getenv("DJANGO_DEBUG")


class SMSSender(ABC):
    @abstractmethod
    def send(self, phone: str, code: str) -> None:
        pass


class ConsoleSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        print(phone, code)


class SMSAeroSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        response = requests.post(
            f"https://{self.EMAIL}:{self.APIKEY}@gate.smsaero.ru/v2/sms/send",
            {
                "number": phone,
                "sign": "SMS Aero",
                "text": f"Служба доставки Tomilov-Delivery.\nВаш код регистрации: {code}",
            },
        )

        print(response)
        print(response.text)


# sms_sender = ConsoleSender()
sms_sender = SMSAeroSender()
