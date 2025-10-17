"""Тесты для репозиториев клиентов."""
import pytest
from src.repositories.customer_repo import CustomerRepository
from src.models.customer import Customer


class TestCustomerRepository:
    """Тесты для репозитория клиентов."""

    def test_repository_creation(self, customer_repository):
        """Тест создания репозитория."""
        assert len(customer_repository.get_all()) == 0

    def test_add_customer(self, customer_repository, sample_customer):
        """Тест добавления клиента в репозиторий."""
        added_customer = customer_repository.add(sample_customer)

        assert added_customer == sample_customer
        assert customer_repository.get_by_id(
            sample_customer.id) == sample_customer

    def test_add_duplicate_customer(self, customer_repository, sample_customer):
        """Тест добавления дублирующегося клиента."""
        customer_repository.add(sample_customer)

        with pytest.raises(ValueError, match=f"Customer with id {sample_customer.id} already exists"):
            customer_repository.add(sample_customer)

    def test_get_by_id_existing(self, customer_repository, sample_customer):
        """Тест получения существующего клиента по ID."""
        customer_repository.add(sample_customer)
        retrieved = customer_repository.get_by_id(sample_customer.id)
        assert retrieved == sample_customer

    def test_get_by_id_nonexistent(self, customer_repository):
        """Тест получения несуществующего клиента."""
        retrieved = customer_repository.get_by_id(999)
        assert retrieved is None

    def test_find_by_email_existing(self, customer_repository, sample_customer):
        """Тест поиска клиента по существующему email."""
        customer_repository.add(sample_customer)
        found = customer_repository.find_by_email(sample_customer.email)
        assert found == sample_customer

    def test_find_by_email_nonexistent(self, customer_repository):
        """Тест поиска клиента по несуществующему email."""
        found = customer_repository.find_by_email("nonexistent@example.com")
        assert found is None

    def test_get_all_empty(self, customer_repository):
        """Тест получения всех клиентов из пустого репозитория."""
        customers = customer_repository.get_all()
        assert len(customers) == 0

    def test_get_all_with_customers(self, customer_repository, sample_customers):
        """Тест получения всех клиентов."""
        for customer in sample_customers:
            customer_repository.add(customer)

        all_customers = customer_repository.get_all()
        assert len(all_customers) == len(sample_customers)

        for customer in sample_customers:
            assert customer in all_customers

    def test_update_existing_customer(self, customer_repository, sample_customer):
        """Тест обновления существующего клиента."""
        customer_repository.add(sample_customer)

        sample_customer.email = "newemail@example.com"
        updated = customer_repository.update(sample_customer)

        assert updated.email == "newemail@example.com"
        retrieved = customer_repository.get_by_id(sample_customer.id)
        assert retrieved.email == "newemail@example.com"

    def test_update_nonexistent_customer(self, customer_repository):
        """Тест обновления несуществующего клиента."""
        nonexistent_customer = Customer(999, "Nonexistent", "test@example.com")

        with pytest.raises(ValueError, match="Customer with id 999 not found"):
            customer_repository.update(nonexistent_customer)

    def test_delete_existing_customer(self, customer_repository, sample_customer):
        """Тест удаления существующего клиента."""
        customer_repository.add(sample_customer)
        customer_repository.delete(sample_customer.id)

        retrieved = customer_repository.get_by_id(sample_customer.id)
        assert retrieved is None

    def test_delete_nonexistent_customer(self, customer_repository):
        """Тест удаления несуществующего клиента."""
        # Не должно вызывать исключение
        customer_repository.delete(999)

    def test_email_search_case_sensitivity(self, customer_repository):
        """Тест чувствительности поиска по email к регистру."""
        customer = Customer(1, "Test User", "Test@Example.Com")
        customer_repository.add(customer)

        # Поиск должен быть точным
        found_exact = customer_repository.find_by_email("Test@Example.Com")
        found_lower = customer_repository.find_by_email("test@example.com")

        assert found_exact == customer
        assert found_lower is None

    def test_multiple_customers_same_name_different_email(self, customer_repository):
        """Тест добавления клиентов с одинаковыми именами, но разными email."""
        customer1 = Customer(1, "John Doe", "john1@example.com")
        customer2 = Customer(2, "John Doe", "john2@example.com")

        customer_repository.add(customer1)
        customer_repository.add(customer2)

        assert len(customer_repository.get_all()) == 2
        assert customer_repository.find_by_email(
            "john1@example.com") == customer1
        assert customer_repository.find_by_email(
            "john2@example.com") == customer2

    def test_repository_independence(self):
        """Тест независимости экземпляров репозитория."""
        repo1 = CustomerRepository()
        repo2 = CustomerRepository()

        customer = Customer(1, "Test", "test@example.com")
        repo1.add(customer)

        assert len(repo1.get_all()) == 1
        assert len(repo2.get_all()) == 0
