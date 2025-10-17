"""Фикстуры для тестов."""
import pytest
from src.models import (
    Product, Customer, Category,
    PercentageDiscount, FixedDiscount,
    StandardDelivery, ExpressDelivery,
    CreditCardPayment, BankTransferPayment, PayPalPayment,
    CartItem, Order, Warehouse
)
from src.repositories import (
    ProductRepository, CustomerRepository, OrderRepository, WarehouseRepository
)
from src.servises import (
    ProductService, CustomerService, CartService, OrderService, ApplicationService
)


@pytest.fixture
def sample_product():
    """Создает тестовый продукт."""
    return Product(product_id=1, name="Test Product", price=100.0)


@pytest.fixture
def sample_products():
    """Создает список тестовых продуктов."""
    return [
        Product(product_id=1, name="Laptop", price=1000.0),
        Product(product_id=2, name="Mouse", price=25.0),
        Product(product_id=3, name="Keyboard", price=75.0),
    ]


@pytest.fixture
def sample_customer():
    """Создает тестового клиента."""
    customer = Customer(id=1, name="John Doe", email="john@example.com")
    customer.add_address("123 Main St", "New York", "USA")
    return customer


@pytest.fixture
def sample_customers():
    """Создает список тестовых клиентов."""
    customers = [
        Customer(id=1, name="John Doe", email="john@example.com"),
        Customer(id=2, name="Jane Smith", email="jane@example.com"),
    ]
    customers[0].add_address("123 Main St", "New York", "USA")
    customers[1].add_address("456 Oak Ave", "Los Angeles", "USA")
    return customers


@pytest.fixture
def sample_category():
    """Создает тестовую категорию."""
    return Category("Electronics")


@pytest.fixture
def sample_cart_items(sample_products):
    """Создает тестовые элементы корзины."""
    return [
        CartItem(sample_products[0], 1),
        CartItem(sample_products[1], 2),
    ]


@pytest.fixture
def sample_percentage_discount():
    """Создает процентную скидку."""
    return PercentageDiscount(10.0)  # 10%


@pytest.fixture
def sample_fixed_discount():
    """Создает фиксированную скидку."""
    return FixedDiscount(50.0)  # $50


@pytest.fixture
def sample_standard_delivery():
    """Создает стандартную доставку."""
    return StandardDelivery()


@pytest.fixture
def sample_express_delivery():
    """Создает экспресс доставку."""
    return ExpressDelivery()


@pytest.fixture
def sample_credit_card_payment():
    """Создает платеж кредитной картой."""
    return CreditCardPayment("1234-5678-9012-3456")


@pytest.fixture
def sample_paypal_payment():
    """Создает PayPal платеж."""
    return PayPalPayment("user@example.com")


@pytest.fixture
def sample_bank_transfer_payment():
    """Создает банковский перевод."""
    return BankTransferPayment("1234567890")


@pytest.fixture
def sample_order(sample_customer, sample_cart_items):
    """Создает тестовый заказ."""
    return Order(sample_customer, sample_cart_items)


@pytest.fixture
def warehouse():
    """Создает склад."""
    return Warehouse()


@pytest.fixture
def product_repository():
    """Создает репозиторий продуктов."""
    return ProductRepository()


@pytest.fixture
def customer_repository():
    """Создает репозиторий клиентов."""
    return CustomerRepository()


@pytest.fixture
def order_repository():
    """Создает репозиторий заказов."""
    return OrderRepository()


@pytest.fixture
def warehouse_repository():
    """Создает репозиторий склада."""
    return WarehouseRepository()


@pytest.fixture
def product_service(product_repository):
    """Создает сервис продуктов."""
    return ProductService(product_repository)


@pytest.fixture
def customer_service(customer_repository):
    """Создает сервис клиентов."""
    return CustomerService(customer_repository)


@pytest.fixture
def cart_service(product_repository):
    """Создает сервис корзины."""
    return CartService(product_repository)


@pytest.fixture
def order_service(order_repository, product_repository, customer_repository):
    """Создает сервис заказов."""
    return OrderService(order_repository, product_repository, customer_repository)


@pytest.fixture
def application_service():
    """Создает основной сервис приложения."""
    return ApplicationService()


@pytest.fixture
def populated_product_repository(product_repository, sample_products):
    """Заполненный репозиторий продуктов."""
    for product in sample_products:
        product_repository.add(product)
    return product_repository


@pytest.fixture
def populated_customer_repository(customer_repository, sample_customers):
    """Заполненный репозиторий клиентов."""
    for customer in sample_customers:
        customer_repository.add(customer)
    return customer_repository


@pytest.fixture
def populated_warehouse(warehouse_repository, sample_products):
    """Заполненный склад."""
    for product in sample_products:
        warehouse_repository.add_stock(product, 100)
    return warehouse_repository
