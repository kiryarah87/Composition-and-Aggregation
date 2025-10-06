"""Тесты для схем (DTO)."""
import pytest
from src.schemas import (
    ProductDTO, CustomerDTO, AddressDTO, CartItemDTO,
    PercentageDiscountDTO, FixedDiscountDTO,
    StandardDeliveryDTO, ExpressDeliveryDTO,
    CreditCardPaymentDTO, BankTransferPaymentDTO, PayPalPaymentDTO,
    OrderCreateDTO
)
from src.models import (
    Product, Customer, CartItem,
    PercentageDiscount, FixedDiscount,
    StandardDelivery, ExpressDelivery,
    CreditCardPayment, BankTransferPayment, PayPalPayment
)


class TestProductDTO:
    """Тесты для ProductDTO."""

    def test_product_dto_creation(self):
        """Тест создания ProductDTO."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)

        assert dto.product_id == 1
        assert dto.name == "Test Product"
        assert dto.price == 100.0

    def test_product_dto_from_model(self, sample_product):
        """Тест создания DTO из модели."""
        dto = ProductDTO.from_model(sample_product)

        assert dto.product_id == sample_product.product_id
        assert dto.name == sample_product.name
        assert dto.price == sample_product.price

    def test_product_dto_to_model(self):
        """Тест создания модели из DTO."""
        dto = ProductDTO(product_id=1, name="Test Product", price=100.0)
        product = dto.to_model()

        assert isinstance(product, Product)
        assert product.product_id == dto.product_id
        assert product.name == dto.name
        assert product.price == dto.price


class TestCustomerDTO:
    """Тесты для CustomerDTO."""

    def test_customer_dto_creation(self):
        """Тест создания CustomerDTO."""
        address_dto = AddressDTO("123 Main St", "New York", "USA")
        dto = CustomerDTO(
            id=1,
            name="John Doe",
            email="john@example.com",
            addresses=[address_dto]
        )

        assert dto.id == 1
        assert dto.name == "John Doe"
        assert dto.email == "john@example.com"
        assert len(dto.addresses) == 1

    def test_customer_dto_from_model(self, sample_customer):
        """Тест создания DTO из модели."""
        dto = CustomerDTO.from_model(sample_customer)

        assert dto.id == sample_customer.id
        assert dto.name == sample_customer.name
        assert dto.email == sample_customer.email
        assert len(dto.addresses) == len(sample_customer.addresses)

    def test_customer_dto_to_model(self):
        """Тест создания модели из DTO."""
        address_dto = AddressDTO("123 Main St", "New York", "USA")
        dto = CustomerDTO(
            id=1,
            name="John Doe",
            email="john@example.com",
            addresses=[address_dto]
        )
        customer = dto.to_model()

        assert isinstance(customer, Customer)
        assert customer.id == dto.id
        assert customer.name == dto.name
        assert customer.email == dto.email
        assert len(customer.addresses) == len(dto.addresses)


class TestCartItemDTO:
    """Тесты для CartItemDTO."""

    def test_cart_item_dto_creation(self):
        """Тест создания CartItemDTO."""
        product_dto = ProductDTO(
            product_id=1, name="Test Product", price=100.0)
        dto = CartItemDTO(product=product_dto, quantity=2)

        assert dto.product == product_dto
        assert dto.quantity == 2

    def test_cart_item_dto_from_model(self, sample_cart_items):
        """Тест создания DTO из модели."""
        cart_item = sample_cart_items[0]
        dto = CartItemDTO.from_model(cart_item)

        assert dto.product.product_id == cart_item.product.product_id
        assert dto.quantity == cart_item.quantity

    def test_cart_item_dto_to_model(self):
        """Тест создания модели из DTO."""
        product_dto = ProductDTO(
            product_id=1, name="Test Product", price=100.0)
        dto = CartItemDTO(product=product_dto, quantity=2)
        cart_item = dto.to_model()

        assert isinstance(cart_item, CartItem)
        assert cart_item.product.product_id == dto.product.product_id
        assert cart_item.quantity == dto.quantity


class TestDiscountDTOs:
    """Тесты для DTO скидок."""

    def test_percentage_discount_dto(self):
        """Тест PercentageDiscountDTO."""
        dto = PercentageDiscountDTO(value=15.0)

        assert dto.value == 15.0
        assert dto.calculate_discount(100.0) == 15.0

        discount = dto.to_model()
        assert isinstance(discount, PercentageDiscount)
        assert discount.percentage == 15.0

    def test_fixed_discount_dto(self):
        """Тест FixedDiscountDTO."""
        dto = FixedDiscountDTO(value=25.0)

        assert dto.value == 25.0
        assert dto.calculate_discount(100.0) == 25.0
        assert dto.calculate_discount(10.0) == 10.0  # min(25, 10)

        discount = dto.to_model()
        assert isinstance(discount, FixedDiscount)
        assert discount.fixed_amount == 25.0


class TestDeliveryDTOs:
    """Тесты для DTO доставки."""

    def test_standard_delivery_dto(self):
        """Тест StandardDeliveryDTO."""
        dto = StandardDeliveryDTO()
        delivery = dto.to_model()

        assert isinstance(delivery, StandardDelivery)
        assert delivery.cost() == 5.0

    def test_express_delivery_dto(self):
        """Тест ExpressDeliveryDTO."""
        dto = ExpressDeliveryDTO()
        delivery = dto.to_model()

        assert isinstance(delivery, ExpressDelivery)
        assert delivery.cost() == 15.0


class TestPaymentDTOs:
    """Тесты для DTO платежей."""

    def test_credit_card_payment_dto(self):
        """Тест CreditCardPaymentDTO."""
        dto = CreditCardPaymentDTO(details="1234-5678-9012-3456")
        payment = dto.to_model()

        assert isinstance(payment, CreditCardPayment)
        assert payment.card_number == "1234-5678-9012-3456"

    def test_bank_transfer_payment_dto(self):
        """Тест BankTransferPaymentDTO."""
        dto = BankTransferPaymentDTO(details="Bank details")
        payment = dto.to_model()

        assert isinstance(payment, BankTransferPayment)

    def test_paypal_payment_dto(self):
        """Тест PayPalPaymentDTO."""
        dto = PayPalPaymentDTO(details="user@example.com")
        payment = dto.to_model()

        assert isinstance(payment, PayPalPayment)
        assert payment.e_mail == "user@example.com"


class TestOrderCreateDTO:
    """Тесты для OrderCreateDTO."""

    def test_order_create_dto_creation(self):
        """Тест создания OrderCreateDTO."""
        dto = OrderCreateDTO(
            customer_id=1,
            items=[(1, 2), (2, 1)],
            discount=PercentageDiscountDTO(value=10.0),
            delivery=StandardDeliveryDTO(),
            payment=CreditCardPaymentDTO(details="1234-5678-9012-3456")
        )

        assert dto.customer_id == 1
        assert len(dto.items) == 2
        assert dto.items[0] == (1, 2)
        assert dto.items[1] == (2, 1)
        assert isinstance(dto.discount, PercentageDiscountDTO)
        assert isinstance(dto.delivery, StandardDeliveryDTO)
        assert isinstance(dto.payment, CreditCardPaymentDTO)

    def test_order_create_dto_to_model(self, sample_customer, sample_cart_items):
        """Тест создания модели заказа из DTO."""
        dto = OrderCreateDTO(
            customer_id=1,
            items=[(1, 2)],
            discount=FixedDiscountDTO(value=50.0),
            delivery=ExpressDeliveryDTO(),
            payment=PayPalPaymentDTO(details="user@example.com")
        )

        order = dto.to_model(sample_customer, sample_cart_items)

        assert order.customer == sample_customer
        assert len(order.items) == len(sample_cart_items)
        assert order.discount is not None
        assert order.delivery is not None
        assert order.payment is not None


class TestDTOEdgeCases:
    """Тесты крайних случаев для DTO."""

    def test_empty_customer_addresses(self):
        """Тест клиента без адресов."""
        dto = CustomerDTO(id=1, name="No Address",
                          email="test@example.com", addresses=[])
        customer = dto.to_model()

        assert len(customer.addresses) == 0

    def test_zero_price_product(self):
        """Тест продукта с нулевой ценой."""
        dto = ProductDTO(product_id=1, name="Free Product", price=0.0)
        product = dto.to_model()

        assert product.price == 0.0

    def test_zero_discount(self):
        """Тест нулевой скидки."""
        dto = PercentageDiscountDTO(value=0.0)
        assert dto.calculate_discount(100.0) == 0.0

        fixed_dto = FixedDiscountDTO(value=0.0)
        assert fixed_dto.calculate_discount(100.0) == 0.0

    def test_large_quantity_cart_item(self):
        """Тест элемента корзины с большим количеством."""
        product_dto = ProductDTO(product_id=1, name="Bulk Item", price=1.0)
        dto = CartItemDTO(product=product_dto, quantity=10000)
        cart_item = dto.to_model()

        assert cart_item.quantity == 10000

    def test_dto_round_trip_conversion(self, sample_product):
        """Тест конвертации DTO туда и обратно."""
        # Product: Model -> DTO -> Model
        dto = ProductDTO.from_model(sample_product)
        product_copy = dto.to_model()

        assert product_copy.product_id == sample_product.product_id
        assert product_copy.name == sample_product.name
        assert product_copy.price == sample_product.price
