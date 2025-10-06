"""Тесты для репозиториев заказов."""
import pytest
from src.repositories.order_repo import OrderRepository
from src.models.order import Order
from src.models.customer import Customer
from src.models.cart import CartItem
from src.models.product import Product


class TestOrderRepository:
    """Тесты для репозитория заказов."""

    def test_repository_creation(self, order_repository):
        """Тест создания репозитория."""
        assert len(order_repository.get_all()) == 0

    def test_add_order(self, order_repository, sample_order):
        """Тест добавления заказа в репозиторий."""
        added_order = order_repository.add(sample_order)

        assert added_order == sample_order
        assert added_order.order_id == 1  # Первый заказ получает ID 1
        assert order_repository.get_by_id(1) == sample_order

    def test_add_multiple_orders_auto_increment_id(self, order_repository):
        """Тест автоинкремента ID при добавлении заказов."""
        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        order1 = Order(customer, cart_items)
        order2 = Order(customer, cart_items)

        added_order1 = order_repository.add(order1)
        added_order2 = order_repository.add(order2)

        assert added_order1.order_id == 1
        assert added_order2.order_id == 2

    def test_get_by_id_existing(self, order_repository, sample_order):
        """Тест получения существующего заказа по ID."""
        order_repository.add(sample_order)
        retrieved = order_repository.get_by_id(sample_order.order_id)
        assert retrieved == sample_order

    def test_get_by_id_nonexistent(self, order_repository):
        """Тест получения несуществующего заказа."""
        retrieved = order_repository.get_by_id(999)
        assert retrieved is None

    def test_get_by_customer_existing(self, order_repository):
        """Тест получения заказов по клиенту."""
        customer1 = Customer(1, "Customer 1", "customer1@example.com")
        customer2 = Customer(2, "Customer 2", "customer2@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        order1 = Order(customer1, cart_items)
        order2 = Order(customer1, cart_items)
        order3 = Order(customer2, cart_items)

        order_repository.add(order1)
        order_repository.add(order2)
        order_repository.add(order3)

        customer1_orders = order_repository.get_by_customer(1)
        customer2_orders = order_repository.get_by_customer(2)

        assert len(customer1_orders) == 2
        assert len(customer2_orders) == 1
        assert order1 in customer1_orders
        assert order2 in customer1_orders
        assert order3 in customer2_orders

    def test_get_by_customer_nonexistent(self, order_repository):
        """Тест получения заказов несуществующего клиента."""
        orders = order_repository.get_by_customer(999)
        assert len(orders) == 0

    def test_get_all_empty(self, order_repository):
        """Тест получения всех заказов из пустого репозитория."""
        orders = order_repository.get_all()
        assert len(orders) == 0

    def test_get_all_with_orders(self, order_repository):
        """Тест получения всех заказов."""
        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        order1 = Order(customer, cart_items)
        order2 = Order(customer, cart_items)

        order_repository.add(order1)
        order_repository.add(order2)

        all_orders = order_repository.get_all()
        assert len(all_orders) == 2
        assert order1 in all_orders
        assert order2 in all_orders

    def test_update_existing_order(self, order_repository, sample_order):
        """Тест обновления существующего заказа."""
        order_repository.add(sample_order)

        from src.enum import OrderStatus
        sample_order.status = OrderStatus.PROCESSING
        updated_order = order_repository.update(sample_order)

        assert updated_order.status == OrderStatus.PROCESSING
        retrieved = order_repository.get_by_id(sample_order.order_id)
        assert retrieved.status == OrderStatus.PROCESSING

    def test_update_nonexistent_order(self, order_repository):
        """Тест обновления несуществующего заказа."""
        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        nonexistent_order = Order(customer, cart_items)
        nonexistent_order.order_id = 999

        with pytest.raises(ValueError, match="Order with id 999 not found"):
            order_repository.update(nonexistent_order)

    def test_order_id_assignment(self, order_repository):
        """Тест правильного присвоения ID заказам."""
        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        order = Order(customer, cart_items)
        assert order.order_id is None  # До добавления в репозиторий

        added_order = order_repository.add(order)
        assert added_order.order_id is not None  # После добавления
        assert added_order.order_id == 1

    def test_repository_independence(self):
        """Тест независимости экземпляров репозитория."""
        repo1 = OrderRepository()
        repo2 = OrderRepository()

        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]
        order = Order(customer, cart_items)

        repo1.add(order)

        assert len(repo1.get_all()) == 1
        assert len(repo2.get_all()) == 0

    def test_id_counter_independence(self):
        """Тест независимости счетчиков ID у разных репозиториев."""
        repo1 = OrderRepository()
        repo2 = OrderRepository()

        customer = Customer(1, "Test Customer", "test@example.com")
        product = Product(1, "Test Product", 100.0)
        cart_items = [CartItem(product, 1)]

        order1 = Order(customer, cart_items)
        order2 = Order(customer, cart_items)

        added1 = repo1.add(order1)
        added2 = repo2.add(order2)

        # Оба должны получить ID = 1, так как репозитории независимы
        assert added1.order_id == 1
        assert added2.order_id == 1
