import logging
from typing import Any
from src.servises import ApplicationService
from src.schemas import (
    OrderCreateDTO,
    PercentageDiscountDTO,
    FixedDiscountDTO,
    StandardDeliveryDTO,
    ExpressDeliveryDTO,
    CreditCardPaymentDTO,
    PayPalPaymentDTO,
    AddressDTO
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecommerce.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DemoRunner:
    """Класс для запуска демонстрации функционала e-commerce системы"""

    def __init__(self, app: ApplicationService):
        self.app = app
        self.products = {}
        self.customers = {}

    def log_separator(self, title: str = ""):
        """Вывод разделителя в лог"""
        if title:
            logger.info(f"{'='*60}")
            logger.info(f"  {title}")
            logger.info(f"{'='*60}\n")
        else:
            logger.info(f"{'-'*60}\n")

    def initialize_data(self) -> None:
        """Инициализация данных из JSON файлов"""
        logger.info("1. LOADING DATA FROM JSON FILES")
        self.log_separator()

        data = self.app.initialize_sample_data()
        self.products = data['products']
        self.customers = data['customers']

        self._log_loaded_products()
        self._log_loaded_customers()

    def _log_loaded_products(self) -> None:
        """Вывод загруженных продуктов"""
        logger.info("Products loaded successfully:")
        all_products = self.app.product_service.get_all_products()
        for product in all_products:
            logger.info(f"   [{product.product_id}] {product.name:<30} ${product.price:>7.2f}")

    def _log_loaded_customers(self) -> None:
        """Вывод загруженных клиентов"""
        logger.info("Customers loaded successfully:")
        all_customers = self.app.customer_service.get_all_customers()
        for customer in all_customers:
            logger.info(f"   {customer.name} ({customer.email})")
            for addr in customer.addresses:
                logger.info(f"      {addr.street}, {addr.city}, {addr.country}")

    def display_product_catalog(self) -> None:
        """Отображение каталога продуктов"""
        self.log_separator()
        logger.info("2. ALL PRODUCTS IN CATALOG")
        self.log_separator()

        all_products = self.app.product_service.get_all_products()
        logger.info(f"Total products: {len(all_products)}\n")
        for product in all_products:
            logger.info(f"   [{product.product_id}] {product.name:<30} ${product.price:>7.2f}")

    def demo_customer_cart(self, customer_key: str, items_to_add: list, section_number: int) -> list:
        """
        Демонстрация работы с корзиной

        Args:
            customer_key: ключ клиента в словаре
            items_to_add: список кортежей (product_key, quantity)
            section_number: номер секции для лога

        Returns:
            список элементов корзины
        """
        self.log_separator()
        logger.info(f"{section_number}. CUSTOMER - SHOPPING CART")
        self.log_separator()

        customer = self.customers.get(customer_key)
        logger.info(f"Customer: {customer.name}")
        logger.info("Adding items to cart...")

        for product_key, quantity in items_to_add:
            product = self.products.get(product_key)
            self.app.cart_service.add_item(product.product_id, quantity)
            logger.info(f"   Added: {product.name} x{quantity}")

        self._display_cart_contents()
        return self.app.cart_service.get_items()

    def _display_cart_contents(self) -> None:
        """Отображение содержимого корзины"""
        logger.info("Cart contents:")
        cart_items = self.app.cart_service.get_items()

        for item in cart_items:
            subtotal = item.product.price * item.quantity
            logger.info(
                f"   {item.product.name:<30} x{item.quantity}  "
                f"${item.product.price:>7.2f}  =  ${subtotal:>8.2f}"
            )

        cart_total = self.app.cart_service.get_total()
        logger.info(f"   {'Cart Total:':<35}                  ${cart_total:>8.2f}")

    def create_order(
        self,
        customer_key: str,
        cart_items: list,
        discount,
        delivery,
        payment,
        section_number: int,
        discount_description: str
    ) -> Any:
        """
        Создание заказа

        Args:
            customer_key: ключ клиента
            cart_items: элементы корзины
            discount: объект скидки
            delivery: объект доставки
            payment: объект оплаты
            section_number: номер секции
            discount_description: описание скидки для лога

        Returns:
            результат создания заказа
        """
        self.log_separator()
        logger.info(f"{section_number}. CREATING ORDER ({discount_description})")
        self.log_separator()

        customer = self.customers.get(customer_key)

        order_dto = OrderCreateDTO(
            customer_id=customer.id,
            items=[(item.product.product_id, item.quantity) for item in cart_items],
            discount=discount,
            delivery=delivery,
            payment=payment
        )

        order_result = self.app.order_service.create_order(order_dto)
        self._log_order_details(order_result, discount_description)

        self.app.cart_service.clear()
        return order_result

    def _log_order_details(self, order_result: Any, discount_description: str) -> None:
        """Вывод деталей заказа"""
        logger.info(f"Order #{order_result.order_id} created successfully!")
        logger.info(f"Customer: {order_result.customer_name}")
        logger.info(f"Status: {order_result.status}")
        logger.info(f"Payment Method: {order_result.payment_method}")
        logger.info("Order items:")

        for item in order_result.items:
            item_total = item.product.price * item.quantity
            logger.info(
                f"   {item.product.name:<30} x{item.quantity}  "
                f"${item.product.price:>7.2f}  =  ${item_total:>8.2f}"
            )

        logger.info(f"{'Subtotal:':<50} ${order_result.subtotal:>8.2f}")
        logger.info(f"{'Discount (' + discount_description + '):':<50} -${order_result.discount_amount:>8.2f}")
        logger.info(f"{'Delivery:':<50} ${order_result.delivery_cost:>8.2f}")
        logger.info(f"{'-'*60}")
        logger.info(f"{'TOTAL:':<50} ${order_result.total_amount:>8.2f}")
        logger.info(f"Payment processed via {order_result.payment_method}")

    def display_all_orders(self) -> None:
        """Отображение всех заказов в системе"""
        self.log_separator()
        logger.info("7. ALL ORDERS IN SYSTEM")
        self.log_separator()

        all_orders = self.app.order_service.get_all_orders()
        logger.info(f"Total orders: {len(all_orders)}\n")

        for order in all_orders:
            logger.info(f"Order #{order.order_id}")
            logger.info(f"   Customer: {order.customer_name}")
            logger.info(f"   Items: {len(order.items)}")
            logger.info(f"   Total: ${order.total_amount:.2f}")
            logger.info(f"   Status: {order.status}\n")

    def display_customer_orders(self) -> None:
        """Отображение заказов конкретных клиентов"""
        self.log_separator()
        logger.info("8. CUSTOMER ORDERS")
        self.log_separator()

        for customer_key in ['john', 'jane']:
            customer = self.customers.get(customer_key)
            customer_orders = self.app.order_service.get_customer_orders(customer.id)

            logger.info(f"{customer.name}'s orders: {len(customer_orders)}")
            for order in customer_orders:
                logger.info(f"   Order #{order.order_id}: ${order.total_amount:.2f} - {order.status}")
            logger.info("")

    def update_product_price(self, product_key: str, new_price: float) -> None:
        """Обновление цены продукта"""
        self.log_separator()
        logger.info("9. UPDATING PRODUCT PRICE")
        self.log_separator()

        product = self.products.get(product_key)
        logger.info(f"Old price for {product.name}: ${product.price:.2f}")

        self.app.product_service.update_price(product.product_id, new_price)
        updated_product = self.app.product_service.get_product(product.product_id)

        logger.info(f"New price for {updated_product.name}: ${updated_product.price:.2f}")
        logger.info("Price updated successfully!")

    def add_customer_address(self, customer_key: str, address_dto: AddressDTO) -> None:
        """Добавление адреса клиенту"""
        self.log_separator()
        logger.info("10. ADDING NEW ADDRESS TO CUSTOMER")
        self.log_separator()

        customer = self.customers.get(customer_key)
        updated_customer = self.app.customer_service.add_address_to_customer(
            customer.id, address_dto
        )

        logger.info(f"Customer: {updated_customer.name}")
        logger.info(f"Total addresses: {len(updated_customer.addresses)}")
        logger.info("All addresses:")

        for i, addr in enumerate(updated_customer.addresses, 1):
            logger.info(f"   {i}. {addr.street}, {addr.city}, {addr.country}")

    def cancel_order(self, order_result: Any) -> None:
        """Отмена заказа"""
        self.log_separator()
        logger.info("11. CANCELLING ORDER")
        self.log_separator()

        logger.info(f"Cancelling Order #{order_result.order_id}...")
        cancelled_order = self.app.order_service.cancel_order(order_result.order_id)
        logger.info(f"Order #{cancelled_order.order_id} status: {cancelled_order.status}")

    def update_customer_email(self, customer_key: str, new_email: str) -> None:
        """Обновление email клиента"""
        self.log_separator()
        logger.info("12. UPDATING CUSTOMER EMAIL")
        self.log_separator()

        customer = self.customers.get(customer_key)
        logger.info(f"Old email: {customer.email}")

        updated_customer = self.app.customer_service.update_customer_email(
            customer.id, new_email
        )

        logger.info(f"New email: {updated_customer.email}")
        logger.info("Email updated successfully!")

    def display_statistics(self) -> None:
        """Отображение финальной статистики"""
        self.log_separator()
        logger.info("13. FINAL STATISTICS")
        self.log_separator()

        stats = self.app.get_statistics()

        logger.info(f"Total Products:     {stats['total_products']}")
        logger.info(f"Total Customers:    {stats['total_customers']}")
        logger.info(f"Total Orders:       {stats['total_orders']}")
        logger.info(f"   Active:           {stats['active_orders']}")
        logger.info(f"   Cancelled:        {stats['cancelled_orders']}")
        logger.info(f"Total Revenue:      ${stats['total_revenue']:.2f}")


def main():
    """Главная функция для запуска демонстрации"""
    app = ApplicationService()
    demo = DemoRunner(app)

    demo.log_separator("E-COMMERCE SYSTEM DEMO")
    demo.initialize_data()
    demo.display_product_catalog()

    cart_items_1 = demo.demo_customer_cart(
        customer_key='john',
        items_to_add=[('dell', 1), ('logitech', 2), ('mechanical', 1)],
        section_number=3
    )

    order1 = demo.create_order(
        customer_key='john',
        cart_items=cart_items_1,
        discount=PercentageDiscountDTO(value=15.0),
        delivery=ExpressDeliveryDTO(),
        payment=CreditCardPaymentDTO(details="4111-1111-1111-1111"),
        section_number=4,
        discount_description="15%"
    )

    cart_items_2 = demo.demo_customer_cart(
        customer_key='jane',
        items_to_add=[('4k', 2), ('wireless', 1), ('mechanical', 2)],
        section_number=5
    )

    demo.create_order(
        customer_key='jane',
        cart_items=cart_items_2,
        discount=FixedDiscountDTO(value=100.0),
        delivery=StandardDeliveryDTO(),
        payment=PayPalPaymentDTO(details="jane.smith@paypal.com"),
        section_number=6,
        discount_description="$100"
    )

    demo.display_all_orders()
    demo.display_customer_orders()
    demo.update_product_price('dell', 1350.0)

    new_address = AddressDTO(street="999 Elm Street", city="Chicago", country="USA")
    demo.add_customer_address('john', new_address)

    demo.cancel_order(order1)
    demo.update_customer_email('jane', "jane.new@example.com")
    demo.display_statistics()
    demo.log_separator("END OF DEMO")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"\nError occurred: {e}")
