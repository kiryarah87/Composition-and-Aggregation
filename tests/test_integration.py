"""Интеграционные тесты для всей системы."""
import pytest
from src.servises.app_service import ApplicationService
from src.schemas import (
    OrderCreateDTO, PercentageDiscountDTO, FixedDiscountDTO,
    StandardDeliveryDTO, ExpressDeliveryDTO, CreditCardPaymentDTO,
    PayPalPaymentDTO, AddressDTO
)
from src.enum import OrderStatus


@pytest.mark.integration
class TestSystemIntegration:
    """Интеграционные тесты системы."""

    @pytest.fixture
    def app_with_data(self):
        """Приложение с загруженными тестовыми данными."""
        app = ApplicationService()
        app.initialize_sample_data()
        return app

    def test_full_order_workflow(self, app_with_data):
        """Тест полного жизненного цикла заказа."""
        # Получаем клиента
        customers = app_with_data.customer_service.get_all_customers()
        assert len(customers) > 0
        customer = customers[0]

        # Получаем продукты
        products = app_with_data.product_service.get_all_products()
        assert len(products) > 0

        # Добавляем товары в корзину
        app_with_data.cart_service.add_item(products[0].product_id, 1)
        if len(products) > 1:
            app_with_data.cart_service.add_item(products[1].product_id, 2)

        cart_items = app_with_data.cart_service.get_items()
        assert len(cart_items) > 0

        # Создаем заказ
        order_items = [(item.product.product_id, item.quantity)
                       for item in cart_items]

        order_dto = OrderCreateDTO(
            customer_id=customer.id,
            items=order_items,
            discount=PercentageDiscountDTO(value=10.0),
            delivery=StandardDeliveryDTO(),
            payment=CreditCardPaymentDTO(details="1234-5678-9012-3456")
        )

        # Создаем заказ через сервис
        result = app_with_data.order_service.create_order(order_dto)

        assert result.order_id is not None
        assert result.customer_name == customer.name
        assert result.status == OrderStatus.PROCESSING
        assert result.total_amount > 0

        # Проверяем, что заказ сохранен
        saved_order = app_with_data.order_service.get_order(result.order_id)
        assert saved_order is not None
        assert saved_order.order_id == result.order_id

    def test_customer_management_workflow(self, app_with_data):
        """Тест управления клиентами."""
        # Создаем нового клиента
        from src.schemas import CustomerDTO
        new_customer_dto = CustomerDTO(
            id=999,
            name="Test Customer",
            email="test@example.com",
            addresses=[]
        )

        created_customer = app_with_data.customer_service.create_customer(
            new_customer_dto)
        assert created_customer.id == 999
        assert created_customer.email == "test@example.com"

        # Добавляем адрес
        address_dto = AddressDTO("123 Test St", "Test City", "Test Country")
        updated_customer = app_with_data.customer_service.add_address_to_customer(
            999, address_dto
        )
        assert len(updated_customer.addresses) == 1

        # Обновляем email
        updated_customer = app_with_data.customer_service.update_customer_email(
            999, "newemail@example.com"
        )
        assert updated_customer.email == "newemail@example.com"

    def test_product_management_workflow(self, app_with_data):
        """Тест управления продуктами."""
        # Создаем новый продукт
        from src.schemas import ProductDTO
        new_product_dto = ProductDTO(
            product_id=999,
            name="Test Product",
            price=99.99
        )

        created_product = app_with_data.product_service.create_product(
            new_product_dto)
        assert created_product.product_id == 999
        assert created_product.price == 99.99

        # Обновляем цену
        app_with_data.product_service.update_price(999, 149.99)
        updated_product = app_with_data.product_service.get_product(999)
        assert updated_product.price == 149.99

        # Удаляем продукт
        app_with_data.product_service.delete_product(999)
        deleted_product = app_with_data.product_service.get_product(999)
        assert deleted_product is None

    def test_order_cancellation_workflow(self, app_with_data):
        """Тест отмены заказа."""
        # Создаем заказ
        customers = app_with_data.customer_service.get_all_customers()
        products = app_with_data.product_service.get_all_products()

        order_dto = OrderCreateDTO(
            customer_id=customers[0].id,
            items=[(products[0].product_id, 1)],
            discount=FixedDiscountDTO(value=10.0),
            delivery=ExpressDeliveryDTO(),
            payment=PayPalPaymentDTO(details="user@example.com")
        )

        created_order = app_with_data.order_service.create_order(order_dto)
        assert created_order.status == OrderStatus.PROCESSING

        # Отменяем заказ
        cancelled_order = app_with_data.order_service.cancel_order(
            created_order.order_id)
        assert cancelled_order.status == OrderStatus.CANCELLED

    def test_cart_to_order_conversion(self, app_with_data):
        """Тест конвертации корзины в заказ."""
        products = app_with_data.product_service.get_all_products()
        customers = app_with_data.customer_service.get_all_customers()

        # Заполняем корзину
        cart_service = app_with_data.cart_service
        cart_service.add_item(products[0].product_id, 2)
        cart_service.add_item(products[1].product_id, 1)

        cart_total = cart_service.get_total()
        cart_items = cart_service.get_items()

        # Создаем заказ на основе корзины
        order_items = [(item.product.product_id, item.quantity)
                       for item in cart_items]

        order_dto = OrderCreateDTO(
            customer_id=customers[0].id,
            items=order_items,
            discount=PercentageDiscountDTO(value=0.0),  # Без скидки
            delivery=StandardDeliveryDTO(),
            payment=CreditCardPaymentDTO(details="1111-2222-3333-4444")
        )

        order_result = app_with_data.order_service.create_order(order_dto)

        # Проверяем, что стоимость корректна (корзина + доставка)
        expected_total = cart_total + 5.0  # 5.0 - стоимость стандартной доставки
        assert order_result.total_amount == expected_total

    def test_multiple_customers_orders(self, app_with_data):
        """Тест заказов от нескольких клиентов."""
        customers = app_with_data.customer_service.get_all_customers()
        products = app_with_data.product_service.get_all_products()

        # Создаем заказы от разных клиентов
        orders = []
        for i, customer in enumerate(customers[:2]):  # Первые два клиента
            order_dto = OrderCreateDTO(
                customer_id=customer.id,
                items=[(products[i % len(products)].product_id, 1)],
                discount=PercentageDiscountDTO(value=5.0),
                delivery=StandardDeliveryDTO(),
                payment=CreditCardPaymentDTO(details=f"1234-{i:04d}-9012-3456")
            )
            order = app_with_data.order_service.create_order(order_dto)
            orders.append(order)

        # Проверяем заказы каждого клиента
        for i, customer in enumerate(customers[:2]):
            customer_orders = app_with_data.order_service.get_customer_orders(
                customer.id)
            assert len(customer_orders) >= 1
            assert any(order.customer_name ==
                       customer.name for order in customer_orders)

    def test_statistics_calculation(self, app_with_data):
        """Тест расчета статистики."""
        # Создаем несколько заказов
        customers = app_with_data.customer_service.get_all_customers()
        products = app_with_data.product_service.get_all_products()

        for i in range(3):
            order_dto = OrderCreateDTO(
                customer_id=customers[0].id,
                items=[(products[0].product_id, 1)],
                discount=PercentageDiscountDTO(value=0.0),
                delivery=StandardDeliveryDTO(),
                payment=CreditCardPaymentDTO(details="1234-5678-9012-3456")
            )
            app_with_data.order_service.create_order(order_dto)

        # Получаем статистику
        stats = app_with_data.get_statistics()

        assert "total_products" in stats
        assert "total_customers" in stats
        assert "total_orders" in stats
        assert "total_revenue" in stats
        assert stats["total_orders"] >= 3

    def test_data_persistence_across_services(self, app_with_data):
        """Тест сохранения данных между сервисами."""
        # Создаем продукт через один сервис
        from src.schemas import ProductDTO
        product_dto = ProductDTO(
            product_id=777, name="Shared Product", price=77.77)
        app_with_data.product_service.create_product(product_dto)

        # Используем его в корзине
        app_with_data.cart_service.add_item(777, 1)
        cart_items = app_with_data.cart_service.get_items()

        # Проверяем, что продукт доступен
        assert len(cart_items) == 1
        assert cart_items[0].product.product_id == 777
        assert cart_items[0].product.name == "Shared Product"

    def test_error_handling_in_workflow(self, app_with_data):
        """Тест обработки ошибок в рабочих процессах."""
        customers = app_with_data.customer_service.get_all_customers()

        # Попытка создать заказ с несуществующим продуктом
        order_dto = OrderCreateDTO(
            customer_id=customers[0].id,
            items=[(99999, 1)],  # Несуществующий продукт
            discount=PercentageDiscountDTO(value=0.0),
            delivery=StandardDeliveryDTO(),
            payment=CreditCardPaymentDTO(details="1234-5678-9012-3456")
        )

        with pytest.raises(ValueError, match="Product with id 99999 not found"):
            app_with_data.order_service.create_order(order_dto)

        # Попытка создать заказ с несуществующим клиентом
        order_dto_bad_customer = OrderCreateDTO(
            customer_id=99999,  # Несуществующий клиент
            items=[(1, 1)],
            discount=PercentageDiscountDTO(value=0.0),
            delivery=StandardDeliveryDTO(),
            payment=CreditCardPaymentDTO(details="1234-5678-9012-3456")
        )

        with pytest.raises(ValueError, match="Customer with id 99999 not found"):
            app_with_data.order_service.create_order(order_dto_bad_customer)
