"""Тесты для моделей доставки."""
import pytest
from src.models.delivery import Delivery, StandardDelivery, ExpressDelivery


class TestStandardDelivery:
    """Тесты для стандартной доставки."""

    def test_standard_delivery_creation(self):
        """Тест создания стандартной доставки."""
        delivery = StandardDelivery()
        assert isinstance(delivery, StandardDelivery)

    def test_standard_delivery_cost(self, sample_standard_delivery):
        """Тест стоимости стандартной доставки."""
        cost = sample_standard_delivery.cost()
        assert cost == 5.0


class TestExpressDelivery:
    """Тесты для экспресс-доставки."""

    def test_express_delivery_creation(self):
        """Тест создания экспресс-доставки."""
        delivery = ExpressDelivery()
        assert isinstance(delivery, ExpressDelivery)

    def test_express_delivery_cost(self, sample_express_delivery):
        """Тест стоимости экспресс-доставки."""
        cost = sample_express_delivery.cost()
        assert cost == 15.0


class TestDeliveryAbstract:
    """Тесты для абстрактного класса Delivery."""

    def test_delivery_cannot_be_instantiated(self):
        """Тест что абстрактный класс нельзя инстанцировать."""
        with pytest.raises(TypeError):
            Delivery()

    def test_delivery_subclass_must_implement_cost(self):
        """Тест что подкласс должен реализовать метод cost."""
        class IncompleteDelivery(Delivery):
            pass

        with pytest.raises(TypeError):
            IncompleteDelivery()

    def test_delivery_proper_inheritance(self, sample_standard_delivery, sample_express_delivery):
        """Тест правильного наследования."""
        assert isinstance(sample_standard_delivery, Delivery)
        assert isinstance(sample_express_delivery, Delivery)

    def test_delivery_cost_comparison(self, sample_standard_delivery, sample_express_delivery):
        """Тест сравнения стоимости доставки."""
        standard_cost = sample_standard_delivery.cost()
        express_cost = sample_express_delivery.cost()

        # Экспресс-доставка должна быть дороже стандартной
        assert express_cost > standard_cost
