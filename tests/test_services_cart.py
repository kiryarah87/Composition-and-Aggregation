"""Тесты для сервисов корзины."""
import pytest
from src.servises.cart_service import CartService
from src.repositories.product_repo import ProductRepository
from src.schemas import CartItemDTO, ProductDTO
from src.models.product import Product


class TestCartService:
    """Тесты для сервиса корзины."""

    def test_cart_service_creation(self, cart_service):
        """Тест создания сервиса корзины."""
        assert cart_service.is_empty()
        assert len(cart_service.get_items()) == 0
        assert cart_service.get_total() == 0.0

    def test_add_item_valid(self, cart_service, populated_product_repository):
        """Тест добавления валидного товара в корзину."""
        cart_service._product_repository = populated_product_repository

        cart_item = cart_service.add_item(1, 2)  # Laptop, qty 2

        assert cart_item.product.product_id == 1
        assert cart_item.quantity == 2
        assert len(cart_service.get_items()) == 1

    def test_add_item_nonexistent_product(self, cart_service):
        """Тест добавления несуществующего продукта."""
        with pytest.raises(ValueError, match="Product with id 999 not found"):
            cart_service.add_item(999, 1)

    def test_add_item_zero_quantity(self, cart_service, populated_product_repository):
        """Тест добавления товара с нулевым количеством."""
        cart_service._product_repository = populated_product_repository

        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart_service.add_item(1, 0)

    def test_add_item_negative_quantity(self, cart_service, populated_product_repository):
        """Тест добавления товара с отрицательным количеством."""
        cart_service._product_repository = populated_product_repository

        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart_service.add_item(1, -1)

    def test_add_same_item_multiple_times(self, cart_service, populated_product_repository):
        """Тест добавления одного товара несколько раз."""
        cart_service._product_repository = populated_product_repository

        # Добавляем товар первый раз
        cart_item1 = cart_service.add_item(1, 2)
        assert cart_item1.quantity == 2
        assert len(cart_service.get_items()) == 1

        # Добавляем тот же товар еще раз
        cart_item2 = cart_service.add_item(1, 3)
        assert cart_item2.quantity == 5  # 2 + 3
        assert len(cart_service.get_items()) == 1  # Все еще один элемент
        assert cart_item1 is cart_item2  # Тот же объект

    def test_add_different_items(self, cart_service, populated_product_repository):
        """Тест добавления разных товаров."""
        cart_service._product_repository = populated_product_repository

        cart_service.add_item(1, 1)  # Laptop
        cart_service.add_item(2, 2)  # Mouse

        items = cart_service.get_items()
        assert len(items) == 2

        product_ids = [item.product.product_id for item in items]
        assert 1 in product_ids
        assert 2 in product_ids

    def test_remove_item_existing(self, cart_service, populated_product_repository):
        """Тест удаления существующего товара из корзины."""
        cart_service._product_repository = populated_product_repository

        cart_service.add_item(1, 2)
        cart_service.add_item(2, 1)
        assert len(cart_service.get_items()) == 2

        cart_service.remove_item(1)
        items = cart_service.get_items()
        assert len(items) == 1
        assert items[0].product.product_id == 2

    def test_remove_item_nonexistent(self, cart_service):
        """Тест удаления несуществующего товара."""
        # Не должно вызывать ошибку
        cart_service.remove_item(999)
        assert cart_service.is_empty()

    def test_update_quantity_existing(self, cart_service, populated_product_repository):
        """Тест обновления количества существующего товара."""
        cart_service._product_repository = populated_product_repository

        cart_service.add_item(1, 2)
        updated_item = cart_service.update_quantity(1, 5)

        assert updated_item.quantity == 5
        items = cart_service.get_items()
        assert len(items) == 1
        assert items[0].quantity == 5

    def test_update_quantity_nonexistent(self, cart_service):
        """Тест обновления количества несуществующего товара."""
        with pytest.raises(ValueError, match="Product with id 999 not in cart"):
            cart_service.update_quantity(999, 5)

    def test_update_quantity_zero(self, cart_service, populated_product_repository):
        """Тест обновления количества до нуля."""
        cart_service._product_repository = populated_product_repository
        cart_service.add_item(1, 2)

        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart_service.update_quantity(1, 0)

    def test_get_total_empty_cart(self, cart_service):
        """Тест получения общей стоимости пустой корзины."""
        assert cart_service.get_total() == 0.0

    def test_get_total_with_items(self, cart_service, populated_product_repository):
        """Тест получения общей стоимости корзины с товарами."""
        cart_service._product_repository = populated_product_repository

        cart_service.add_item(1, 1)  # Laptop: 1000 * 1 = 1000
        cart_service.add_item(2, 2)  # Mouse: 25 * 2 = 50

        total = cart_service.get_total()
        assert total == 1050.0

    def test_clear_cart(self, cart_service, populated_product_repository):
        """Тест очистки корзины."""
        cart_service._product_repository = populated_product_repository

        cart_service.add_item(1, 1)
        cart_service.add_item(2, 2)
        assert not cart_service.is_empty()

        cart_service.clear()
        assert cart_service.is_empty()
        assert len(cart_service.get_items()) == 0
        assert cart_service.get_total() == 0.0

    def test_is_empty_states(self, cart_service, populated_product_repository):
        """Тест проверки пустоты корзины в различных состояниях."""
        cart_service._product_repository = populated_product_repository

        # Изначально пустая
        assert cart_service.is_empty()

        # После добавления товара
        cart_service.add_item(1, 1)
        assert not cart_service.is_empty()

        # После удаления всех товаров
        cart_service.remove_item(1)
        assert cart_service.is_empty()

    def test_get_items_immutability(self, cart_service, populated_product_repository):
        """Тест неизменяемости возвращаемого списка товаров."""
        cart_service._product_repository = populated_product_repository
        cart_service.add_item(1, 1)

        items = cart_service.get_items()
        original_length = len(items)

        # Изменение полученного списка не должно влиять на корзину
        items.clear()

        assert len(cart_service.get_items()) == original_length

    def test_cart_workflow(self, cart_service, populated_product_repository):
        """Тест полного рабочего процесса корзины."""
        cart_service._product_repository = populated_product_repository

        # Добавляем товары
        cart_service.add_item(1, 1)  # Laptop
        cart_service.add_item(2, 3)  # Mouse x3
        cart_service.add_item(3, 2)  # Keyboard x2

        # Проверяем состояние
        assert len(cart_service.get_items()) == 3
        expected_total = 1000.0 + (25.0 * 3) + \
            (75.0 * 2)  # 1000 + 75 + 150 = 1225
        assert cart_service.get_total() == expected_total

        # Обновляем количество
        cart_service.update_quantity(2, 1)  # Mouse x1
        new_total = 1000.0 + 25.0 + 150.0  # 1175
        assert cart_service.get_total() == new_total

        # Удаляем товар
        cart_service.remove_item(3)  # Remove keyboard
        assert len(cart_service.get_items()) == 2
        final_total = 1000.0 + 25.0  # 1025
        assert cart_service.get_total() == final_total
