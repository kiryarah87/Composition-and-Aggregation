from dataclasses import dataclass
from abc import ABC, abstractmethod
from .models import (
    Product,
    Customer,
    CartItem,
    Order,
    StandardDelivery,
    ExpressDelivery,
    CreditCardPayment,
    BankTransferPayment,
    PayPalPayment,
    PercentageDiscount,
    FixedDiscount,
    Payment,
)
from .enum import OrderStatus


@dataclass
class ProductDTO:
    """Data Transfer Object for Product"""
    product_id: int
    name: str
    price: float

    @classmethod
    def from_model(cls, product: Product) -> 'ProductDTO':
        return cls(
            product_id=product.product_id,
            name=product.name,
            price=product.price
        )

    def to_model(self) -> Product:
        return Product(
            product_id=self.product_id,
            name=self.name,
            price=self.price
        )


@dataclass
class AddressDTO:
    """Data Transfer Object for Address"""
    street: str
    city: str
    country: str


@dataclass
class CustomerDTO:
    """Data Transfer Object for Customer"""
    id: int
    name: str
    email: str
    addresses: list[AddressDTO]

    @classmethod
    def from_model(cls, customer: Customer) -> 'CustomerDTO':
        return cls(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            addresses=[
                AddressDTO(addr.street, addr.city, addr.country)
                for addr in customer.addresses
            ]
        )

    def to_model(self) -> Customer:
        customer = Customer(self.id, self.name, self.email)
        for addr_dto in self.addresses:
            customer.add_address(
                addr_dto.street, addr_dto.city, addr_dto.country)
        return customer


@dataclass
class CartItemDTO:
    """Data Transfer Object for Cart Item"""
    product: ProductDTO
    quantity: int

    @classmethod
    def from_model(cls, cart_item: CartItem) -> 'CartItemDTO':
        return cls(
            product=ProductDTO.from_model(cart_item.product),
            quantity=cart_item.quantity
        )

    def to_model(self) -> CartItem:
        return CartItem(self.product.to_model(), self.quantity)


@dataclass
class DiscountDTO(ABC):
    """Base DTO for discounts"""
    value: float

    @abstractmethod
    def calculate_discount(self, amount: float) -> float:
        """Calculate discount amount"""
        pass

    @abstractmethod
    def to_model(self):
        """Convert to domain model"""
        pass


@dataclass
class PercentageDiscountDTO(DiscountDTO):
    """DTO for percentage discount"""

    def calculate_discount(self, amount: float) -> float:
        return amount * (self.value / 100)

    def to_model(self) -> PercentageDiscount:
        return PercentageDiscount(self.value)


@dataclass
class FixedDiscountDTO(DiscountDTO):
    """DTO for fixed amount discount"""

    def calculate_discount(self, amount: float) -> float:
        return min(self.value, amount)

    def to_model(self) -> FixedDiscount:
        return FixedDiscount(self.value)


@dataclass
class DeliveryDTO(ABC):
    """Base DTO for delivery methods"""

    @abstractmethod
    def to_model(self):
        """Convert to domain model"""
        pass


@dataclass
class StandardDeliveryDTO(DeliveryDTO):
    """DTO for standard delivery"""

    def to_model(self) -> StandardDelivery:
        return StandardDelivery()


@dataclass
class ExpressDeliveryDTO(DeliveryDTO):
    """DTO for express delivery"""

    def to_model(self) -> ExpressDelivery:
        return ExpressDelivery()


@dataclass
class PaymentDTO(ABC):
    """Base DTO for payment methods"""
    details: str

    @abstractmethod
    def to_model(self):
        """Convert to domain model"""
        pass


@dataclass
class CreditCardPaymentDTO(PaymentDTO):
    """DTO for credit card payment"""

    def to_model(self) -> CreditCardPayment:
        return CreditCardPayment(self.details)


@dataclass
class BankTransferPaymentDTO(PaymentDTO):
    """DTO for bank transfer payment"""

    def to_model(self) -> BankTransferPayment:
        return BankTransferPayment(self.details)


@dataclass
class PayPalPaymentDTO(PaymentDTO):
    """DTO for PayPal payment"""

    def to_model(self) -> PayPalPayment:
        return PayPalPayment(self.details)


@dataclass
class OrderCreateDTO:
    """DTO for creating an order"""
    customer_id: int
    items: list[tuple[int, int]]
    discount: DiscountDTO
    delivery: DeliveryDTO
    payment: PaymentDTO

    def to_model(self, customer, cart_items) -> Order:
        """Convert to Order model"""
        order = Order(
            customer=customer,
            cart_items=cart_items,
        )

        order.discount = self.discount.to_model()
        order.delivery = self.delivery.to_model()
        order.payment = self.payment.to_model()
        return order


@dataclass
class OrderResultDTO:
    """Result of order processing"""
    order_id: int
    customer_name: str
    items: list[CartItemDTO]
    subtotal: float
    discount_amount: float
    delivery_cost: float
    total_amount: float
    status: OrderStatus
    payment_method: Payment | None = None

    @classmethod
    def from_model(cls, order: Order) -> 'OrderResultDTO':
        """Convert Order model to DTO"""
        items_dto = []
        for order_item in order.items:
            product_dto = ProductDTO.from_model(order_item.product)
            cart_item_dto = CartItemDTO(
                product=product_dto, quantity=order_item.quantity
            )
            items_dto.append(cart_item_dto)

        subtotal = (
            sum(item.product.price * item.quantity for item in order.items)
        )
        discount_amount = (
            order.discount.apply(subtotal) if order.discount else 0
        )
        delivery_cost = order.delivery.cost() if order.delivery else 0
        total = subtotal - discount_amount + delivery_cost

        return cls(
            order_id=order.order_id,
            customer_name=order.customer.name,
            items=items_dto,
            subtotal=subtotal,
            discount_amount=discount_amount,
            delivery_cost=delivery_cost,
            total_amount=total,
            status=order.status,
            payment_method=order.payment
        )
