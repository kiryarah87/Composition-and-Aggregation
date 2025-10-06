from models.order import Order


class OrderRepository:
    def __init__(self):
        self._orders: dict[int, Order] = {}
        self._next_id: int = 1

    def add(self, order: Order) -> int:
        '''Adds a new order to the repository and returns its ID.'''
        order_id = self._next_id
        self._orders[order_id] = order
        self._next_id += 1
        return order_id

    def get_by_id(self, order_id: int) -> Order | None:
        '''Retrieves an order by its ID.'''
        return self._orders.get(order_id)

    def get_by_customer(self, customer_id: int) -> list[Order]:
        '''Retrieves all orders for a specific customer.'''
        return [
            order for order in self._orders.values()
            if order.customer.id == customer_id
        ]

    def get_all(self) -> list[Order]:
        '''Retrieves all orders in the repository.'''
        return list(self._orders.values())
