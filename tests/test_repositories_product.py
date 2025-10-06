"""Тесты для репозиториев продуктов."""
import pytest
from src.repositories.product_repo import ProductRepository
from src.models.product import Product


class TestProductRepository:
    """Тесты для репозитория продуктов."""

    def test_repository_creation(self, product_repository):
        """Тест создания репозитория."""
        assert len(product_repository.get_all()) == 0

    def test_create_product(self, product_repository):
        """Тест создания продукта через репозиторий."""
        product = product_repository.create(1, "Test Product", 100.0)

        assert product.product_id == 1
        assert product.name == "Test Product"
        assert product.price == 100.0
        assert product_repository.get_by_id(1) == product

    def test_add_product(self, product_repository, sample_product):
        """Тест добавления продукта в репозиторий."""
        product_repository.add(sample_product)
        retrieved = product_repository.get_by_id(sample_product.product_id)
        assert retrieved == sample_product

    def test_get_by_id_existing(self, product_repository, sample_product):
        """Тест получения существующего продукта по ID."""
        product_repository.add(sample_product)
        retrieved = product_repository.get_by_id(sample_product.product_id)
        assert retrieved == sample_product

    def test_get_by_id_nonexistent(self, product_repository):
        """Тест получения несуществующего продукта."""
        retrieved = product_repository.get_by_id(999)
        assert retrieved is None

    def test_get_all_empty(self, product_repository):
        """Тест получения всех продуктов из пустого репозитория."""
        products = product_repository.get_all()
        assert len(products) == 0

    def test_get_all_with_products(self, product_repository, sample_products):
        """Тест получения всех продуктов."""
        for product in sample_products:
            product_repository.add(product)

        all_products = product_repository.get_all()
        assert len(all_products) == len(sample_products)

        for product in sample_products:
            assert product in all_products

    def test_update_existing_product(self, product_repository, sample_product):
        """Тест обновления существующего продукта."""
        product_repository.add(sample_product)

        sample_product.price = 150.0
        product_repository.update(sample_product)

        updated = product_repository.get_by_id(sample_product.product_id)
        assert updated.price == 150.0

    def test_update_nonexistent_product(self, product_repository):
        """Тест обновления несуществующего продукта."""
        nonexistent_product = Product(999, "Nonexistent", 100.0)

        with pytest.raises(ValueError, match="Product with id 999 not found"):
            product_repository.update(nonexistent_product)

    def test_delete_existing_product(self, product_repository, sample_product):
        """Тест удаления существующего продукта."""
        product_repository.add(sample_product)
        product_repository.delete(sample_product.product_id)

        retrieved = product_repository.get_by_id(sample_product.product_id)
        assert retrieved is None

    def test_delete_nonexistent_product(self, product_repository):
        """Тест удаления несуществующего продукта."""
        with pytest.raises(ValueError, match="Product with id 999 not found"):
            product_repository.delete(999)

    def test_multiple_operations(self, product_repository):
        """Тест множественных операций с репозиторием."""
        # Создание
        product1 = product_repository.create(1, "Product 1", 100.0)
        product2 = product_repository.create(2, "Product 2", 200.0)

        # Проверка
        assert len(product_repository.get_all()) == 2

        # Обновление
        product1.price = 150.0
        product_repository.update(product1)

        # Удаление
        product_repository.delete(2)

        # Финальная проверка
        assert len(product_repository.get_all()) == 1
        assert product_repository.get_by_id(1).price == 150.0
        assert product_repository.get_by_id(2) is None

    def test_repository_independence(self):
        """Тест независимости экземпляров репозитория."""
        repo1 = ProductRepository()
        repo2 = ProductRepository()

        product = Product(1, "Test", 100.0)
        repo1.add(product)

        assert len(repo1.get_all()) == 1
        assert len(repo2.get_all()) == 0
