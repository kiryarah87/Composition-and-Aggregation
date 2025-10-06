from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class CreditCardPayment(Payment):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float):
        print(f"Paid {amount} using credit card {self.card_number}")


class BankTransferPayment(Payment):
    def __init__(self, bank_account: str):
        self.bank_account = bank_account

    def pay(self, amount: float):
        print(f"Paid {amount} via bank transfer")


class PayPalPayment(Payment):
    def __init__(self, e_mail: str):
        self.e_mail = e_mail

    def pay(self, amount: float):
        print(f"Paid {amount} using PayPal")
