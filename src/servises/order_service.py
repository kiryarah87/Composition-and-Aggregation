from ..repositories import OrderRepository, ProductRepository, CustomerRepository
from ..schemas import OrderCreateDTO, OrderResultDTO, CartItemDTO, ProductDTO
from ..enum import OrderStatus


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        customer_repository: CustomerRepository
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._customer_repository = customer_repository

    def create_order(self, order_dto: OrderCreateDTO) -> OrderResultDTO:
        """Create a new order from DTO."""
        customer = self._customer_repository.get_by_id(order_dto.customer_id)
        if not customer:
            raise ValueError(f"Customer with id {order_dto.customer_id} not found")

        cart_items_dto = []
        for product_id, quantity in order_dto.items:
            product = self._product_repository.get_by_id(product_id)

            if not product:
                raise ValueError(f"Product with id {product_id} not found")

            if quantity <= 0:
                raise ValueError(f"Invalid quantity {quantity} for product {product_id}")

            product_dto = ProductDTO.from_model(product)
            cart_item_dto = CartItemDTO(product=product_dto, quantity=quantity)
            cart_items_dto.append(cart_item_dto)

        if not cart_items_dto:
            raise ValueError("Order must contain at least one item")

        cart_items = [item.to_model() for item in cart_items_dto]

        order = order_dto.to_model(customer, cart_items)
        saved_order = self._order_repository.add(order)

        return OrderResultDTO.from_model(saved_order)

    def get_order(self, order_id: int) -> OrderResultDTO | None:
        """Get order by ID."""
        order = self._order_repository.get_by_id(order_id)

        if not order:
            return None
        return OrderResultDTO.from_model(order)

    def get_customer_orders(self, customer_id: int) -> list[OrderResultDTO]:
        """Get all orders for a customer."""
        orders = self._order_repository.get_by_customer(customer_id)
        return [OrderResultDTO.from_model(order) for order in orders]

    def get_all_orders(self) -> list[OrderResultDTO]:
        """Get all orders."""
        orders = self._order_repository.get_all()
        return [OrderResultDTO.from_model(order) for order in orders]

    def cancel_order(self, order_id: int) -> OrderResultDTO:
        """Cancel an order."""
        order = self._order_repository.get_by_id(order_id)

        if not order:
            raise ValueError(f"Order with id {order_id} not found")

        order.status = OrderStatus.CANCELLED
        self._order_repository.update(order)

        return OrderResultDTO.from_model(order)
