from ..models import Customer


class CustomerRepository:
    def __init__(self):
        self._customers: dict[int, Customer] = {}

    def add(self, customer: Customer) -> Customer:
        """Add a customer to the repository."""
        if customer.id in self._customers:
            raise ValueError(f"Customer with id {customer.id} already exists")
        self._customers[customer.id] = customer
        return customer

    def get_by_id(self, customer_id: int) -> Customer | None:
        """Get a customer by ID."""
        return self._customers.get(customer_id)

    def find_by_email(self, email: str) -> Customer | None:
        """Find a customer by email."""
        for customer in self._customers.values():
            if customer.email == email:
                return customer
        return None

    def get_all(self) -> list[Customer]:
        """Get all customers."""
        return list(self._customers.values())

    def update(self, customer: Customer) -> Customer:
        """Update an existing customer."""
        if customer.id not in self._customers:
            raise ValueError(f"Customer with id {customer.id} not found")
        self._customers[customer.id] = customer
        return customer

    def delete(self, customer_id: int) -> None:
        """Delete a customer by ID."""
        if customer_id in self._customers:
            del self._customers[customer_id]
