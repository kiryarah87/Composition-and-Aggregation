from src.repositories.product_repo import ProductRepository
from src.repositories.customer_repo import CustomerRepository
from src.repositories.order_repo import OrderRepository

from src.servises.product_service import ProductService
from src.servises.customer_service import CustomerService
from src.servises.cart_service import CartService
from src.servises.order_service import OrderService

from src.schemas import (
    ProductDTO,
    CustomerDTO,
    AddressDTO,
    OrderCreateDTO,
    PercentageDiscountDTO,
    FixedDiscountDTO,
    StandardDeliveryDTO,
    ExpressDeliveryDTO,
    CreditCardPaymentDTO,
    PayPalPaymentDTO
)


def print_separator(title: str = ""):
    """Print a nice separator line"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'-'*60}\n")


def main():
    # ========== Инициализация репозиториев ==========
    product_repo = ProductRepository()
    customer_repo = CustomerRepository()
    order_repo = OrderRepository()

    # ========== Инициализация сервисов ==========
    product_service = ProductService(product_repo)
    customer_service = CustomerService(customer_repo)
    cart_service = CartService(product_repo)
    order_service = OrderService(order_repo, product_repo, customer_repo)

    print_separator("E-COMMERCE SYSTEM DEMO")

    # ========== 1. СОЗДАНИЕ ПРОДУКТОВ ==========
    print("1. CREATING PRODUCTS")
    print_separator()

    laptop_dto = ProductDTO(product_id=1, name="Dell XPS 15 Laptop", price=1500.0)
    mouse_dto = ProductDTO(product_id=2, name="Logitech MX Master Mouse", price=99.0)
    keyboard_dto = ProductDTO(product_id=3, name="Mechanical Keyboard", price=150.0)
    monitor_dto = ProductDTO(product_id=4, name="4K Monitor", price=450.0)
    headphones_dto = ProductDTO(product_id=5, name="Wireless Headphones", price=250.0)

    laptop = product_service.create_product(laptop_dto)
    mouse = product_service.create_product(mouse_dto)
    keyboard = product_service.create_product(keyboard_dto)
    monitor = product_service.create_product(monitor_dto)
    headphones = product_service.create_product(headphones_dto)

    print("Products created:")
    for product in [laptop, mouse, keyboard, monitor, headphones]:
        print(f"   [{product.product_id}] {product.name:<30} ${product.price:>7.2f}")

    # ========== 2. СПИСОК ВСЕХ ПРОДУКТОВ ==========
    print_separator()
    print("2. ALL PRODUCTS IN CATALOG")
    print_separator()

    all_products = product_service.get_all_products()
    print(f"Total products: {len(all_products)}\n")
    for prod in all_products:
        print(f"   [{prod.product_id}] {prod.name:<30} ${prod.price:>7.2f}")

    # ========== 3. СОЗДАНИЕ КЛИЕНТОВ ==========
    print_separator()
    print("3. CREATING CUSTOMERS")
    print_separator()

    customer1_dto = CustomerDTO(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        addresses=[
            AddressDTO(street="123 Main St", city="New York", country="USA")
        ]
    )

    customer2_dto = CustomerDTO(
        id=2,
        name="Jane Smith",
        email="jane.smith@example.com",
        addresses=[
            AddressDTO(street="456 Oak Ave", city="Los Angeles", country="USA"),
            AddressDTO(street="789 Pine Rd", city="San Francisco", country="USA")
        ]
    )

    customer1 = customer_service.create_customer(customer1_dto)
    customer2 = customer_service.create_customer(customer2_dto)

    print("Customers created:")
    print(f"   {customer1.name} ({customer1.email})")
    for addr in customer1.addresses:
        print(f"      {addr.street}, {addr.city}, {addr.country}")

    print(f"\n   {customer2.name} ({customer2.email})")
    for addr in customer2.addresses:
        print(f"      {addr.street}, {addr.city}, {addr.country}")

    # ========== 4. РАБОТА С КОРЗИНОЙ (Клиент 1) ==========
    print_separator()
    print("4. CUSTOMER 1 - SHOPPING CART")
    print_separator()

    print(f"Customer: {customer1.name}")
    print("\nAdding items to cart...")

    cart_service.add_item(laptop.product_id, 1)
    print(f"   Added: {laptop.name} x1")

    cart_service.add_item(mouse.product_id, 2)
    print(f"   Added: {mouse.name} x2")

    cart_service.add_item(keyboard.product_id, 1)
    print(f"   Added: {keyboard.name} x1")

    print("\nCart contents:")
    cart_items = cart_service.get_items()
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        print(f"   {item.product.name:<30} x{item.quantity}  ${item.product.price:>7.2f}  =  ${subtotal:>8.2f}")

    cart_total = cart_service.get_total()
    print(f"\n   {'Cart Total:':<35}                  ${cart_total:>8.2f}")

    # ========== 5. СОЗДАНИЕ ЗАКАЗА 1 (с процентной скидкой) ==========
    print_separator()
    print("5. CREATING ORDER #1 (Percentage Discount)")
    print_separator()

    order1_dto = OrderCreateDTO(
        customer_id=customer1.id,
        items=[(item.product.product_id, item.quantity) for item in cart_items],
        discount=PercentageDiscountDTO(value=15.0),
        delivery=ExpressDeliveryDTO(),
        payment=CreditCardPaymentDTO(details="4111-1111-1111-1111")
    )

    order1_result = order_service.create_order(order1_dto)

    print(f"Order #{order1_result.order_id} created successfully!")
    print(f"Customer: {order1_result.customer_name}")
    print(f"Status: {order1_result.status}")
    print("\nOrder items:")
    for item in order1_result.items:
        item_total = item.product.price * item.quantity
        print(f"   {item.product.name:<30} x{item.quantity}  ${item.product.price:>7.2f}  =  ${item_total:>8.2f}")

    print(f"\n{'Subtotal:':<50} ${order1_result.subtotal:>8.2f}")
    print(f"{'Discount (15%):':<50} -${order1_result.discount_amount:>8.2f}")
    print(f"{'Express Delivery:':<50} ${order1_result.delivery_cost:>8.2f}")
    print(f"{'-'*60}")
    print(f"{'TOTAL:':<50} ${order1_result.total_amount:>8.2f}")

    # Очищаем корзину
    cart_service.clear()

    # ========== 6. РАБОТА С КОРЗИНОЙ (Клиент 2) ==========
    print_separator()
    print("🛒 6. CUSTOMER 2 - SHOPPING CART")
    print_separator()

    print(f"Customer: {customer2.name}")
    print("\nAdding items to cart...")

    cart_service.add_item(monitor.product_id, 2)
    print(f"   Added: {monitor.name} x2")

    cart_service.add_item(headphones.product_id, 1)
    print(f"   Added: {headphones.name} x1")

    cart_service.add_item(keyboard.product_id, 2)
    print(f"   Added: {keyboard.name} x2")

    print("\nCart contents:")
    cart_items = cart_service.get_items()
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        print(f"   {item.product.name:<30} x{item.quantity}  ${item.product.price:>7.2f}  =  ${subtotal:>8.2f}")

    cart_total = cart_service.get_total()
    print(f"\n   {'Cart Total:':<35}                  ${cart_total:>8.2f}")

    # ========== 7. СОЗДАНИЕ ЗАКАЗА 2 (с фиксированной скидкой) ==========
    print_separator()
    print("7. CREATING ORDER #2 (Fixed Discount)")
    print_separator()

    order2_dto = OrderCreateDTO(
        customer_id=customer2.id,
        items=[(item.product.product_id, item.quantity) for item in cart_items],
        discount=FixedDiscountDTO(value=100.0),
        delivery=StandardDeliveryDTO(),
        payment=PayPalPaymentDTO(details="jane.smith@paypal.com")
    )

    order2_result = order_service.create_order(order2_dto)

    print(f"Order #{order2_result.order_id} created successfully!")
    print(f"Customer: {order2_result.customer_name}")
    print(f"Status: {order2_result.status}")
    print("\nOrder items:")
    for item in order2_result.items:
        item_total = item.product.price * item.quantity
        print(f"   {item.product.name:<30} x{item.quantity}  ${item.product.price:>7.2f}  =  ${item_total:>8.2f}")

    print(f"\n{'Subtotal:':<50} ${order2_result.subtotal:>8.2f}")
    print(f"{'Discount ($100):':<50} -${order2_result.discount_amount:>8.2f}")
    print(f"{'Standard Delivery:':<50} ${order2_result.delivery_cost:>8.2f}")
    print(f"{'-'*60}")
    print(f"{'TOTAL:':<50} ${order2_result.total_amount:>8.2f}")

    # ========== 8. ПРОСМОТР ВСЕХ ЗАКАЗОВ ==========
    print_separator()
    print("8. ALL ORDERS IN SYSTEM")
    print_separator()

    all_orders = order_service.get_all_orders()
    print(f"Total orders: {len(all_orders)}\n")

    for order in all_orders:
        print(f"Order #{order.order_id}")
        print(f"   Customer: {order.customer_name}")
        print(f"   Items: {len(order.items)}")
        print(f"   Total: ${order.total_amount:.2f}")
        print(f"   Status: {order.status}\n")

    # ========== 9. ЗАКАЗЫ КОНКРЕТНОГО КЛИЕНТА ==========
    print_separator()
    print("9. CUSTOMER ORDERS")
    print_separator()

    customer1_orders = order_service.get_customer_orders(customer1.id)
    print(f"{customer1.name}'s orders: {len(customer1_orders)}")
    for order in customer1_orders:
        print(f"   Order #{order.order_id}: ${order.total_amount:.2f} - {order.status}")

    print()
    customer2_orders = order_service.get_customer_orders(customer2.id)
    print(f"{customer2.name}'s orders: {len(customer2_orders)}")

    for order in customer2_orders:
        print(f"   Order #{order.order_id}: ${order.total_amount:.2f} - {order.status}")

    # ========== 10. ОБНОВЛЕНИЕ ЦЕНЫ ПРОДУКТА ==========
    print_separator()
    print("10. UPDATING PRODUCT PRICE")
    print_separator()

    print(f"Old price for {laptop.name}: ${laptop.price:.2f}")
    product_service.update_price(laptop.product_id, 1350.0)
    updated_laptop = product_service.get_product(laptop.product_id)
    print(f"New price for {updated_laptop.name}: ${updated_laptop.price:.2f}")
    print("Price updated successfully!")

    # ========== 11. ДОБАВЛЕНИЕ АДРЕСА КЛИЕНТУ ==========
    print_separator()
    print("11. ADDING NEW ADDRESS TO CUSTOMER")
    print_separator()

    new_address = AddressDTO(street="999 Elm Street", city="Chicago", country="USA")
    updated_customer = customer_service.add_address_to_customer(customer1.id, new_address)

    print(f"Customer: {updated_customer.name}")
    print(f"Total addresses: {len(updated_customer.addresses)}")
    print("\nAll addresses:")

    for i, addr in enumerate(updated_customer.addresses, 1):
        print(f"   {i}. {addr.street}, {addr.city}, {addr.country}")

    # ========== 12. ОТМЕНА ЗАКАЗА ==========
    print_separator()
    print("12. CANCELLING ORDER")
    print_separator()

    print(f"Cancelling Order #{order1_result.order_id}...")
    cancelled_order = order_service.cancel_order(order1_result.order_id)
    print(f"Order #{cancelled_order.order_id} status: {cancelled_order.status}")

    # ========== 13. ОБНОВЛЕНИЕ EMAIL КЛИЕНТА ==========
    print_separator()
    print("13. UPDATING CUSTOMER EMAIL")
    print_separator()

    print(f"Old email: {customer2.email}")
    updated_customer2 = customer_service.update_customer_email(customer2.id, "jane.new@example.com")
    print(f"New email: {updated_customer2.email}")
    print("Email updated successfully!")

    # ========== 14. ФИНАЛЬНАЯ СТАТИСТИКА ==========
    print_separator()
    print("14. FINAL STATISTICS")
    print_separator()

    all_products = product_service.get_all_products()
    all_customers = customer_service.get_all_customers()
    all_orders = order_service.get_all_orders()

    total_revenue = sum(order.total_amount for order in all_orders)
    active_orders = [order for order in all_orders if order.status != "cancelled"]
    cancelled_orders = [order for order in all_orders if order.status == "cancelled"]

    print(f"Total Products:     {len(all_products)}")
    print(f"Total Customers:    {len(all_customers)}")
    print(f"Total Orders:       {len(all_orders)}")
    print(f"   Active:           {len(active_orders)}")
    print(f"   Cancelled:        {len(cancelled_orders)}")
    print(f"Total Revenue:      ${total_revenue:.2f}")

    print_separator("END OF DEMO")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
