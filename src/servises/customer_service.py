from ..repositories import CustomerRepository
from ..schemas import CustomerDTO, AddressDTO


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, customer_dto: CustomerDTO) -> CustomerDTO:
        """Create a new customer."""
        existing_customer = self._repository.find_by_email(customer_dto.email)
        if existing_customer:
            raise ValueError(f"Customer with email {customer_dto.email} already exists")

        customer = customer_dto.to_model()
        created_customer = self._repository.add(customer)
        return CustomerDTO.from_model(created_customer)

    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        """Retrieve a customer by ID."""
        customer = self._repository.get_by_id(customer_id)
        return CustomerDTO.from_model(customer) if customer else None

    def get_customer_by_email(self, email: str) -> CustomerDTO | None:
        """Retrieve a customer by email."""
        customer = self._repository.find_by_email(email)
        return CustomerDTO.from_model(customer) if customer else None

    def add_address_to_customer(self, customer_id: int, address_dto: AddressDTO) -> CustomerDTO:
        """Add a new address to a customer."""
        customer = self._repository.get_by_id(customer_id)

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")

        customer.add_address(address_dto.street, address_dto.city, address_dto.country)
        self._repository.update(customer)

        return CustomerDTO.from_model(customer)

    def update_customer_email(self, customer_id: int, new_email: str) -> CustomerDTO:
        """Update customer's email."""
        customer = self._repository.get_by_id(customer_id)

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")

        existing = self._repository.find_by_email(new_email)
        if existing and existing.id != customer_id:
            raise ValueError(f"Email {new_email} is already in use")

        customer.email = new_email
        self._repository.update(customer)

        return CustomerDTO.from_model(customer)

    def get_all_customers(self) -> list[CustomerDTO]:
        """Retrieve all customers."""
        customers = self._repository.get_all()
        return [CustomerDTO.from_model(c) for c in customers]

    def delete_customer(self, customer_id: int) -> None:
        """Delete a customer."""
        customer = self._repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")

        self._repository.delete(customer_id)
