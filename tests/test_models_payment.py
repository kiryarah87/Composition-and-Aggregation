"""Тесты для моделей платежей."""
import pytest
from src.models.payment import Payment, CreditCardPayment, BankTransferPayment, PayPalPayment


class TestCreditCardPayment:
    """Тесты для платежа кредитной картой."""

    def test_credit_card_payment_creation(self):
        """Тест создания платежа кредитной картой."""
        payment = CreditCardPayment("1234-5678-9012-3456")
        assert payment.card_number == "1234-5678-9012-3456"

    def test_credit_card_payment_pay(self, sample_credit_card_payment, capsys):
        """Тест процесса платежа кредитной картой."""
        amount = 100.0
        sample_credit_card_payment.pay(amount)

        captured = capsys.readouterr()
        expected_output = "Paid 100.0 using credit card 1234-5678-9012-3456\n"
        assert captured.out == expected_output


class TestBankTransferPayment:
    """Тесты для банковского перевода."""

    def test_bank_transfer_payment_creation(self):
        """Тест создания банковского перевода."""
        payment = BankTransferPayment("1234567890")
        assert isinstance(payment, BankTransferPayment)

    def test_bank_transfer_payment_pay(self, sample_bank_transfer_payment, capsys):
        """Тест процесса банковского перевода."""
        amount = 250.0
        sample_bank_transfer_payment.pay(amount)

        captured = capsys.readouterr()
        expected_output = "Paid 250.0 via bank transfer\n"
        assert captured.out == expected_output


class TestPayPalPayment:
    """Тесты для PayPal платежа."""

    def test_paypal_payment_creation(self):
        """Тест создания PayPal платежа."""
        payment = PayPalPayment("user@example.com")
        assert payment.e_mail == "user@example.com"

    def test_paypal_payment_pay(self, sample_paypal_payment, capsys):
        """Тест процесса PayPal платежа."""
        amount = 75.5
        sample_paypal_payment.pay(amount)

        captured = capsys.readouterr()
        expected_output = "Paid 75.5 using PayPal\n"
        assert captured.out == expected_output


class TestPaymentAbstract:
    """Тесты для абстрактного класса Payment."""

    def test_payment_cannot_be_instantiated(self):
        """Тест что абстрактный класс нельзя инстанцировать."""
        with pytest.raises(TypeError):
            Payment()

    def test_payment_subclass_must_implement_pay(self):
        """Тест что подкласс должен реализовать метод pay."""
        class IncompletePayment(Payment):
            pass

        with pytest.raises(TypeError):
            IncompletePayment()

    def test_payment_proper_inheritance(self, sample_credit_card_payment, sample_paypal_payment, sample_bank_transfer_payment):
        """Тест правильного наследования."""
        assert isinstance(sample_credit_card_payment, Payment)
        assert isinstance(sample_paypal_payment, Payment)
        assert isinstance(sample_bank_transfer_payment, Payment)

    def test_payment_polymorphism(self, capsys):
        """Тест полиморфизма платежных методов."""
        payments = [
            CreditCardPayment("1111-2222-3333-4444"),
            BankTransferPayment("1234567890"),
            PayPalPayment("test@example.com")
        ]

        amount = 100.0
        for payment in payments:
            payment.pay(amount)

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')

        assert "credit card" in output_lines[0]
        assert "bank transfer" in output_lines[1]
        assert "PayPal" in output_lines[2]
