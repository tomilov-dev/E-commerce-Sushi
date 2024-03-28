import requests
from abc import ABC, abstractmethod


class SMSSender(ABC):
    @abstractmethod
    def send(self, phone: str, code: str) -> None:
        pass


class ConsoleSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        print(phone, code)


class GreenSMSSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        print(phone, code)

        response = requests.post(
            "https://api3.greensms.ru/sms/send",
            data={
                "user": "ivantomilov",
                "pass": "Parad228Hurt",
                "to": "89012207967",
                "txt": "Test message",
                "from": "GREENSMS",
            },
        )
        print(response)


class SMSAeroSender(SMSSender):
    APIKEY = "iSYx37ct6NnxXFmMzi8s3Q1sp0cHQAd9"
    EMAIL = "tomilov.vana@gmail.com"

    def send(self, phone: str, code: str) -> None:
        print(phone, code)

        response = requests.post(
            f"https://{self.EMAIL}:{self.APIKEY}@gate.smsaero.ru/v2/sms/send",
            {
                "number": "89012207967",
                "sign": "SMS Aero",
                "text": "Служба доставки Pizzaro.\nВаш код регистрации: 605913",
            },
        )

        print(response)
        print(response.text)


# sms_sender = GreenSMSSender()
# sms_sender = SMSAeroSender()

sms_sender = ConsoleSender()

if __name__ == "__main__":
    sms_sender.send("1", "2")
