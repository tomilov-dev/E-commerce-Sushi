from abc import ABC, abstractmethod


class SMSSender(ABC):
    @abstractmethod
    def send(self, phone: str, code: str) -> None:
        pass


class ConsoleSender(SMSSender):
    def send(self, phone: str, code: str) -> None:
        print(phone, code)


sms_sender = ConsoleSender()
