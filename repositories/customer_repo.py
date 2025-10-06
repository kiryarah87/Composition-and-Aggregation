from models.customer import Customer


class CustomerRepository:
    def __init__(self):
        self._customers: dict[int, Customer] = {}

    def add(self, customer: Customer) -> None:
        self._customers[customer.id] = customer

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self._customers.get(customer_id)

    def get_all(self) -> list[Customer]:
        return list(self._customers.values())

    def update(self, customer: Customer) -> None:
        if customer.id in self._customers:
            self._customers[customer.id] = customer
        else:
            raise ValueError(f"Customer with id {customer.id} not found")
