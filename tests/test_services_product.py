"""Тесты для сервисов продуктов."""
import pytest
from src.servises.product_service import ProductService
from src.schemas import ProductDTO


class TestProductService:
    """Тесты для сервиса продуктов."""

    def test_create_product_valid(self, product_service):
        """Тест создания валидного продукта."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        result = product_service.create_product(dto)

        assert result.product_id == 1
        assert result.name == "Test Product"
        assert result.price == 100.0

    def test_create_product_negative_price(self, product_service):
        """Тест создания продукта с отрицательной ценой."""
        dto = ProductDTO(product_id=1, name="Test Product", price=-10.0)

        with pytest.raises(ValueError, match="Price cannot be negative"):
            product_service.create_product(dto)

    def test_get_product_existing(self, product_service):
        """Тест получения существующего продукта."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        product_service.create_product(dto)

        result = product_service.get_product(1)
        assert result is not None
        assert result.product_id == 1
        assert result.name == "Test Product"
        assert result.price == 100.0

    def test_get_product_nonexistent(self, product_service):
        """Тест получения несуществующего продукта."""
        result = product_service.get_product(999)
        assert result is None

    def test_update_price_valid(self, product_service):
        """Тест обновления цены продукта."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        product_service.create_product(dto)

        product_service.update_price(1, 150.0)

        updated_product = product_service.get_product(1)
        assert updated_product.price == 150.0

    def test_update_price_negative(self, product_service):
        """Тест обновления цены на отрицательную."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        product_service.create_product(dto)

        with pytest.raises(ValueError, match="Price cannot be negative"):
            product_service.update_price(1, -50.0)

    def test_update_price_nonexistent_product(self, product_service):
        """Тест обновления цены несуществующего продукта."""
        with pytest.raises(ValueError, match="Product with id 999 not found"):
            product_service.update_price(999, 100.0)

    def test_get_all_products_empty(self, product_service):
        """Тест получения всех продуктов из пустого сервиса."""
        products = product_service.get_all_products()
        assert len(products) == 0

    def test_get_all_products_with_data(self, product_service):
        """Тест получения всех продуктов."""
        dto1 = ProductDTO(product_id=1, name="Product 1", price=100.0)
        dto2 = ProductDTO(product_id=2, name="Product 2", price=200.0)

        product_service.create_product(dto1)
        product_service.create_product(dto2)

        products = product_service.get_all_products()
        assert len(products) == 2

        product_ids = [p.product_id for p in products]
        assert 1 in product_ids
        assert 2 in product_ids

    def test_delete_product_existing(self, product_service):
        """Тест удаления существующего продукта."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        product_service.create_product(dto)

        product_service.delete_product(1)

        result = product_service.get_product(1)
        assert result is None

    def test_delete_product_nonexistent(self, product_service):
        """Тест удаления несуществующего продукта."""
        with pytest.raises(ValueError, match="Product with id 999 not found"):
            product_service.delete_product(999)

    def test_service_with_populated_repository(self, populated_product_repository):
        """Тест сервиса с заранее заполненным репозиторием."""
        service = ProductService(populated_product_repository)

        products = service.get_all_products()
        assert len(products) == 3  # Из фикстуры sample_products

        # Проверим, что можем получить конкретные продукты
        laptop = service.get_product(1)
        assert laptop is not None
        assert laptop.name == "Laptop"

    def test_product_dto_conversion(self, product_repository):
        """Тест конвертации между моделью и DTO."""
        service = ProductService(product_repository)
        original_dto = ProductDTO(
            product_id=1, name="Test Product", price=100.0)

        # Создаем продукт через сервис
        created_dto = service.create_product(original_dto)

        # Проверяем, что получили правильный DTO обратно
        assert created_dto.product_id == original_dto.product_id
        assert created_dto.name == original_dto.name
        assert created_dto.price == original_dto.price

        # Проверяем, что продукт действительно сохранен
        retrieved_dto = service.get_product(1)
        assert retrieved_dto == created_dto

    def test_price_validation_edge_cases(self, product_service):
        """Тест валидации цены в крайних случаях."""
        # Нулевая цена допустима
        dto_zero = ProductDTO(product_id=1, name="Free Product", price=0.0)
        result = product_service.create_product(dto_zero)
        assert result.price == 0.0

        # Очень большая цена
        dto_large = ProductDTO(
            product_id=2, name="Expensive Product", price=999999.99)
        result = product_service.create_product(dto_large)
        assert result.price == 999999.99

        # Обновление цены до нуля
        product_service.update_price(1, 0.0)
        updated = product_service.get_product(1)
        assert updated.price == 0.0
