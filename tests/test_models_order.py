"""Тесты для моделей заказов."""
import pytest
from src.models.order import Order, OrderItem, Warehouse
from src.enum import OrderStatus


class TestOrder:
    """Тесты для класса Order."""

    def test_order_creation(self, sample_customer, sample_cart_items):
        """Тест создания заказа."""
        order = Order(sample_customer, sample_cart_items)

        assert order.customer == sample_customer
        assert len(order.items) == len(sample_cart_items)
        assert order.status == OrderStatus.PENDING
        assert order.order_id is None
        assert order.discount is None
        assert order.delivery is None
        assert order.payment is None

    def test_order_id_setter(self, sample_order):
        """Тест установки ID заказа."""
        sample_order.order_id = 123
        assert sample_order.order_id == 123

    def test_order_id_setter_negative(self, sample_order):
        """Тест установки отрицательного ID заказа."""
        with pytest.raises(ValueError, match="Order ID must be positive"):
            sample_order.order_id = -1

    def test_order_id_setter_zero(self, sample_order):
        """Тест установки нулевого ID заказа."""
        with pytest.raises(ValueError, match="Order ID must be positive"):
            sample_order.order_id = 0

    def test_order_status_setter(self, sample_order):
        """Тест установки статуса заказа."""
        sample_order.status = OrderStatus.PROCESSING
        assert sample_order.status == OrderStatus.PROCESSING

    def test_order_discount_setter(self, sample_order, sample_percentage_discount):
        """Тест установки скидки."""
        sample_order.discount = sample_percentage_discount
        assert sample_order.discount == sample_percentage_discount

    def test_order_delivery_setter(self, sample_order, sample_standard_delivery):
        """Тест установки доставки."""
        sample_order.delivery = sample_standard_delivery
        assert sample_order.delivery == sample_standard_delivery

    def test_order_payment_setter(self, sample_order, sample_credit_card_payment):
        """Тест установки платежа."""
        sample_order.payment = sample_credit_card_payment
        assert sample_order.payment == sample_credit_card_payment

    def test_calculate_subtotal(self, sample_order):
        """Тест расчета промежуточной суммы."""
        # Ожидаемая сумма: (1000 * 1) + (25 * 2) = 1050
        subtotal = sample_order._calculate_subtotal()
        assert subtotal == 1050.0

    def test_calculate_total_no_discount_no_delivery(self, sample_order):
        """Тест расчета общей суммы без скидки и доставки."""
        total = sample_order.calculate_total()
        assert total == 1050.0

    def test_calculate_total_with_percentage_discount(self, sample_order, sample_percentage_discount):
        """Тест расчета с процентной скидкой."""
        sample_order.discount = sample_percentage_discount
        # Сумма: 1050, скидка 10% = 105, итого: 945
        total = sample_order.calculate_total()
        assert total == 945.0

    def test_calculate_total_with_fixed_discount(self, sample_order, sample_fixed_discount):
        """Тест расчета с фиксированной скидкой."""
        sample_order.discount = sample_fixed_discount
        # Сумма: 1050, скидка 50, итого: 1000
        total = sample_order.calculate_total()
        assert total == 1000.0

    def test_calculate_total_with_delivery(self, sample_order, sample_standard_delivery):
        """Тест расчета с доставкой."""
        sample_order.delivery = sample_standard_delivery
        # Сумма: 1050, доставка: 5, итого: 1055
        total = sample_order.calculate_total()
        assert total == 1055.0

    def test_calculate_total_complete(self, sample_order, sample_percentage_discount, sample_express_delivery):
        """Тест полного расчета с скидкой и доставкой."""
        sample_order.discount = sample_percentage_discount
        sample_order.delivery = sample_express_delivery
        # Сумма: 1050, скидка 10% = 105, доставка: 15, итого: 960
        total = sample_order.calculate_total()
        assert total == 960.0

    def test_process_payment_success(self, sample_order, sample_credit_card_payment):
        """Тест успешной обработки платежа."""
        sample_order.payment = sample_credit_card_payment
        # Не должно вызвать исключение
        sample_order.process_payment()

    def test_process_payment_no_payment_method(self, sample_order):
        """Тест обработки платежа без метода оплаты."""
        with pytest.raises(ValueError, match="Payment method not set"):
            sample_order.process_payment()


class TestOrderItem:
    """Тесты для класса OrderItem."""

    def test_order_item_creation(self, sample_product):
        """Тест создания элемента заказа."""
        order_item = OrderItem(sample_product, 3)

        assert order_item.product == sample_product
        assert order_item.quantity == 3

    def test_order_item_zero_quantity(self, sample_product):
        """Тест создания элемента с нулевым количеством."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(sample_product, 0)

    def test_order_item_negative_quantity(self, sample_product):
        """Тест создания элемента с отрицательным количеством."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(sample_product, -1)

    def test_get_total_price(self, sample_product):
        """Тест расчета общей стоимости элемента."""
        order_item = OrderItem(sample_product, 2)
        # 100.0 * 2 = 200.0
        assert order_item.get_total_price() == 200.0


class TestWarehouse:
    """Тесты для класса Warehouse."""

    def test_warehouse_creation(self):
        """Тест создания склада."""
        warehouse = Warehouse()
        assert len(warehouse.stock) == 0

    def test_add_stock(self, warehouse, sample_product):
        """Тест добавления товара на склад."""
        warehouse.add_stock(sample_product, 10)
        assert warehouse.stock[sample_product] == 10

    def test_add_stock_existing_product(self, warehouse, sample_product):
        """Тест добавления товара, который уже есть на складе."""
        warehouse.add_stock(sample_product, 10)
        warehouse.add_stock(sample_product, 5)
        assert warehouse.stock[sample_product] == 15

    def test_add_stock_zero_quantity(self, warehouse, sample_product):
        """Тест добавления нулевого количества."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            warehouse.add_stock(sample_product, 0)

    def test_add_stock_negative_quantity(self, warehouse, sample_product):
        """Тест добавления отрицательного количества."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            warehouse.add_stock(sample_product, -5)

    def test_remove_stock(self, warehouse, sample_product):
        """Тест удаления товара со склада."""
        warehouse.add_stock(sample_product, 10)
        warehouse.remove_stock(sample_product, 3)
        assert warehouse.stock[sample_product] == 7

    def test_remove_stock_insufficient(self, warehouse, sample_product):
        """Тест удаления товара при недостаточном количестве."""
        warehouse.add_stock(sample_product, 5)
        with pytest.raises(ValueError, match="Insufficient stock"):
            warehouse.remove_stock(sample_product, 10)

    def test_remove_stock_nonexistent_product(self, warehouse, sample_product):
        """Тест удаления несуществующего товара."""
        with pytest.raises(ValueError, match="Insufficient stock"):
            warehouse.remove_stock(sample_product, 1)

    def test_remove_stock_zero_quantity(self, warehouse, sample_product):
        """Тест удаления нулевого количества."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            warehouse.remove_stock(sample_product, 0)

    def test_remove_stock_negative_quantity(self, warehouse, sample_product):
        """Тест удаления отрицательного количества."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            warehouse.remove_stock(sample_product, -1)

    def test_stock_property_immutable(self, warehouse, sample_product):
        """Тест неизменяемости свойства stock."""
        warehouse.add_stock(sample_product, 10)
        stock_dict = warehouse.stock

        # Изменение полученного словаря должно влиять на исходный
        # (так как возвращается ссылка на оригинал)
        stock_dict[sample_product] = 20
        assert warehouse.stock[sample_product] == 20
