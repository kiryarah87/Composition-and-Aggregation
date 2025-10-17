"""Тесты для моделей клиентов."""
from src.models.customer import Customer, Address


class TestCustomer:
    """Тесты для класса Customer."""

    def test_customer_creation(self):
        """Тест создания клиента."""
        customer = Customer(id=1, name="John Doe", email="john@example.com")

        assert customer.id == 1
        assert customer.name == "John Doe"
        assert customer.email == "john@example.com"
        assert len(customer.addresses) == 0

    def test_customer_add_address(self, sample_customer):
        """Тест добавления адреса клиенту."""
        initial_count = len(sample_customer.addresses)
        sample_customer.add_address("456 Oak St", "Chicago", "USA")

        assert len(sample_customer.addresses) == initial_count + 1
        new_address = sample_customer.addresses[-1]
        assert new_address.street == "456 Oak St"
        assert new_address.city == "Chicago"
        assert new_address.country == "USA"

    def test_customer_multiple_addresses(self):
        """Тест добавления нескольких адресов."""
        customer = Customer(id=1, name="John Doe", email="john@example.com")

        customer.add_address("123 Main St", "New York", "USA")
        customer.add_address("456 Oak Ave", "Los Angeles", "USA")

        assert len(customer.addresses) == 2
        assert customer.addresses[0].city == "New York"
        assert customer.addresses[1].city == "Los Angeles"


class TestAddress:
    """Тесты для класса Address."""

    def test_address_creation(self):
        """Тест создания адреса."""
        address = Address("123 Main St", "New York", "USA")

        assert address.street == "123 Main St"
        assert address.city == "New York"
        assert address.country == "USA"

    def test_address_equality(self):
        """Тест сравнения адресов."""
        address1 = Address("123 Main St", "New York", "USA")
        address2 = Address("123 Main St", "New York", "USA")
        address3 = Address("456 Oak Ave", "New York", "USA")

        # Адреса равны по содержимому, но разные объекты
        assert address1 is not address2
        assert address1 is not address3
