from .customer import Customer
from .cart import CartItem
from .product import Product
from .discount import Discount
from .delivery import Delivery
from .payment import Payment
from ..enum import OrderStatus


class Order:
    '''Represents a customer's order'''
    def __init__(
        self,
        customer: Customer,
        cart_items: list[CartItem],
    ):
        self.customer = customer
        self.items: list[OrderItem] = [
            OrderItem(item.product, item.quantity) for item in cart_items
        ]

        self._status: OrderStatus = OrderStatus.PENDING
        self._order_id: int | None = None
        self._discount: Discount | None = None
        self._delivery: Delivery | None = None
        self._payment: Payment | None = None

    @property
    def order_id(self) -> int | None:
        return self._order_id

    @order_id.setter
    def order_id(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Order ID must be positive")
        self._order_id = value

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, value: OrderStatus) -> None:
        self._status = value

    @property
    def discount(self) -> Discount | None:
        return self._discount

    @discount.setter
    def discount(self, discount: Discount) -> None:
        self._discount = discount

    @property
    def delivery(self) -> Delivery | None:
        return self._delivery

    @delivery.setter
    def delivery(self, delivery: Delivery) -> None:
        '''Sets the delivery method for the order'''
        self._delivery = delivery

    @property
    def payment(self) -> Payment | None:
        return self._payment

    @payment.setter
    def payment(self, payment: Payment) -> None:
        '''Sets the payment method for the order'''
        self._payment = payment

    def calculate_total(self) -> float:
        '''Calculates the total cost of the order'''
        subtotal = self._calculate_subtotal()
        discount_amount = self.discount.apply(subtotal) if self.discount else 0
        delivery_cost = self._delivery.cost() if self._delivery else 0
        return subtotal - discount_amount + delivery_cost

    def _calculate_subtotal(self) -> float:
        '''Calculates the subtotal before discounts and delivery'''
        return sum(item.product.price * item.quantity for item in self.items)

    def process_payment(self) -> None:
        '''Processes the payment for the order'''
        if not self._payment:
            raise ValueError("Payment method not set")
        self._payment.pay(self.calculate_total())


class OrderItem:
    '''Represents an item in an order'''
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.product = product
        self.quantity = quantity

    def get_total_price(self) -> float:
        '''Calculates the total price for this item'''
        return self.product.price * self.quantity


class Warehouse:
    '''Manages product stock levels'''
    def __init__(self):
        self._stock: dict[Product, int] = {}

    @property
    def stock(self) -> dict[Product, int]:
        return self._stock

    def add_stock(self, product: Product, quantity: int) -> None:
        '''Adds stock for a product'''
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._stock[product] = self._stock.get(product, 0) + quantity

    def remove_stock(self, product: Product, quantity: int) -> None:
        '''Removes stock for a product'''
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        current_stock = self._stock.get(product, 0)
        if current_stock < quantity:
            raise ValueError(
                f"Insufficient stock: {current_stock} available, {quantity} requested"
            )
        self._stock[product] -= quantity
