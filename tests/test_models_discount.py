"""Тесты для моделей скидок."""
import pytest
from src.models.discount import Discount, PercentageDiscount, FixedDiscount


class TestPercentageDiscount:
    """Тесты для процентной скидки."""

    def test_percentage_discount_creation(self):
        """Тест создания процентной скидки."""
        discount = PercentageDiscount(15.0)
        assert discount.percentage == 15.0

    def test_percentage_discount_apply(self, sample_percentage_discount):
        """Тест применения процентной скидки."""
        amount = 100.0
        discount_amount = sample_percentage_discount.apply(amount)
        # 10% от 100 = 10
        assert discount_amount == 10.0

    def test_percentage_discount_apply_zero_amount(self, sample_percentage_discount):
        """Тест применения скидки к нулевой сумме."""
        discount_amount = sample_percentage_discount.apply(0.0)
        assert discount_amount == 0.0

    def test_percentage_discount_large_amount(self):
        """Тест применения скидки к большой сумме."""
        discount = PercentageDiscount(25.0)
        amount = 1000.0
        discount_amount = discount.apply(amount)
        # 25% от 1000 = 250
        assert discount_amount == 250.0

    def test_percentage_discount_zero_percent(self):
        """Тест применения нулевой скидки."""
        discount = PercentageDiscount(0.0)
        amount = 100.0
        discount_amount = discount.apply(amount)
        assert discount_amount == 0.0


class TestFixedDiscount:
    """Тесты для фиксированной скидки."""

    def test_fixed_discount_creation(self):
        """Тест создания фиксированной скидки."""
        discount = FixedDiscount(25.0)
        assert discount.fixed_amount == 25.0

    def test_fixed_discount_apply_normal(self, sample_fixed_discount):
        """Тест применения фиксированной скидки к обычной сумме."""
        amount = 100.0
        discount_amount = sample_fixed_discount.apply(amount)
        # min(50, 100) = 50
        assert discount_amount == 50.0

    def test_fixed_discount_apply_small_amount(self, sample_fixed_discount):
        """Тест применения скидки к малой сумме."""
        amount = 30.0
        discount_amount = sample_fixed_discount.apply(amount)
        # min(50, 30) = 30
        assert discount_amount == 30.0

    def test_fixed_discount_apply_zero_amount(self, sample_fixed_discount):
        """Тест применения скидки к нулевой сумме."""
        discount_amount = sample_fixed_discount.apply(0.0)
        assert discount_amount == 0.0

    def test_fixed_discount_large_discount(self):
        """Тест большой фиксированной скидки."""
        discount = FixedDiscount(1000.0)
        amount = 500.0
        discount_amount = discount.apply(amount)
        # min(1000, 500) = 500
        assert discount_amount == 500.0

    def test_fixed_discount_zero_discount(self):
        """Тест нулевой фиксированной скидки."""
        discount = FixedDiscount(0.0)
        amount = 100.0
        discount_amount = discount.apply(amount)
        assert discount_amount == 0.0


class TestDiscountAbstract:
    """Тесты для абстрактного класса Discount."""

    def test_discount_cannot_be_instantiated(self):
        """Тест что абстрактный класс нельзя инстанцировать."""
        with pytest.raises(TypeError):
            Discount()

    def test_discount_subclass_must_implement_apply(self):
        """Тест что подкласс должен реализовать метод apply."""
        class IncompleteDiscount(Discount):
            pass

        with pytest.raises(TypeError):
            IncompleteDiscount()

    def test_discount_proper_inheritance(self, sample_percentage_discount, sample_fixed_discount):
        """Тест правильного наследования."""
        assert isinstance(sample_percentage_discount, Discount)
        assert isinstance(sample_fixed_discount, Discount)
