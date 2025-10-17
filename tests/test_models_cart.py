"""Тесты для моделей корзины."""
from src.models.cart import ShoppingCart, CartItem
from src.models.product import Product


class TestShoppingCart:
    """Тесты для класса ShoppingCart."""

    def test_shopping_cart_creation(self):
        """Тест создания корзины."""
        cart = ShoppingCart()
        assert len(cart.items) == 0

    def test_add_item_to_cart(self):
        """Тест добавления товара в корзину."""
        cart = ShoppingCart()
        product = Product(1, "Test Product", 100.0)

        cart.add_item(product, 2)

        assert len(cart.items) == 1
        assert cart.items[0].product == product
        assert cart.items[0].quantity == 2

    def test_add_multiple_items(self, sample_products):
        """Тест добавления нескольких товаров."""
        cart = ShoppingCart()

        cart.add_item(sample_products[0], 1)
        cart.add_item(sample_products[1], 3)

        assert len(cart.items) == 2
        assert cart.items[0].quantity == 1
        assert cart.items[1].quantity == 3


class TestCartItem:
    """Тесты для класса CartItem."""

    def test_cart_item_creation(self, sample_product):
        """Тест создания элемента корзины."""
        cart_item = CartItem(sample_product, 2)

        assert cart_item.product == sample_product
        assert cart_item.quantity == 2

    def test_cart_item_properties(self):
        """Тест свойств элемента корзины."""
        product = Product(1, "Test Product", 50.0)
        cart_item = CartItem(product, 3)

        assert cart_item.product.product_id == 1
        assert cart_item.product.name == "Test Product"
        assert cart_item.product.price == 50.0
        assert cart_item.quantity == 3

    def test_cart_item_with_zero_quantity(self, sample_product):
        """Тест элемента корзины с нулевым количеством."""
        # CartItem не проверяет количество, это делается на уровне сервисов
        cart_item = CartItem(sample_product, 0)
        assert cart_item.quantity == 0

    def test_cart_item_with_negative_quantity(self, sample_product):
        """Тест элемента корзины с отрицательным количеством."""
        # CartItem не проверяет количество, это делается на уровне сервисов
        cart_item = CartItem(sample_product, -1)
        assert cart_item.quantity == -1
