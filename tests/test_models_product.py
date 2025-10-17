"""Тесты для моделей продуктов."""
import pytest
from src.models.product import Product, Category


class TestProduct:
    """Тесты для класса Product."""

    def test_product_creation(self):
        """Тест создания продукта."""
        product = Product(product_id=1, name="Test Product", price=100.0)

        assert product.product_id == 1
        assert product.name == "Test Product"
        assert product.price == 100.0

    def test_product_price_getter(self, sample_product):
        """Тест получения цены продукта."""
        assert sample_product.price == 100.0

    def test_product_price_setter_valid(self, sample_product):
        """Тест установки валидной цены."""
        sample_product.price = 150.0
        assert sample_product.price == 150.0

    def test_product_price_setter_negative(self, sample_product):
        """Тест установки отрицательной цены."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            sample_product.price = -10.0

    def test_product_price_setter_zero(self, sample_product):
        """Тест установки нулевой цены."""
        sample_product.price = 0.0
        assert sample_product.price == 0.0

    def test_product_equality(self):
        """Тест сравнения продуктов."""
        product1 = Product(1, "Test", 100.0)
        product2 = Product(1, "Test", 100.0)
        product3 = Product(2, "Test", 100.0)

        # Продукты с одинаковыми ID должны быть равны по ссылке
        assert product1 is not product2
        assert product1 is not product3


class TestCategory:
    """Тесты для класса Category."""

    def test_category_creation(self):
        """Тест создания категории."""
        category = Category("Electronics")

        assert category.name == "Electronics"
        assert len(category.products) == 0

    def test_category_add_product(self, sample_category, sample_product):
        """Тест добавления продукта в категорию."""
        sample_category.add_product(sample_product)

        assert len(sample_category.products) == 1
        assert sample_product in sample_category.products

    def test_category_add_duplicate_product(self, sample_category, sample_product):
        """Тест добавления дублирующегося продукта."""
        sample_category.add_product(sample_product)
        sample_category.add_product(sample_product)  # Дубликат

        assert len(sample_category.products) == 1

    def test_category_remove_product(self, sample_category, sample_product):
        """Тест удаления продукта из категории."""
        sample_category.add_product(sample_product)
        sample_category.remove_product(sample_product)

        assert len(sample_category.products) == 0
        assert sample_product not in sample_category.products

    def test_category_remove_nonexistent_product(self, sample_category, sample_product):
        """Тест удаления несуществующего продукта."""
        # Не должно вызывать ошибку
        sample_category.remove_product(sample_product)
        assert len(sample_category.products) == 0

    def test_category_products_immutable(self, sample_category, sample_product):
        """Тест неизменяемости списка продуктов."""
        sample_category.add_product(sample_product)
        products = sample_category.products

        # Изменение полученного списка не должно влиять на категорию
        products.clear()
        assert len(sample_category.products) == 1

    def test_category_multiple_products(self, sample_category, sample_products):
        """Тест добавления нескольких продуктов."""
        for product in sample_products:
            sample_category.add_product(product)

        assert len(sample_category.products) == len(sample_products)
        for product in sample_products:
            assert product in sample_category.products
