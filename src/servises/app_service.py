from pathlib import Path
from ..repositories import (
    ProductRepository,
    CustomerRepository,
    OrderRepository,
    WarehouseRepository
)
from . import ProductService, CustomerService, CartService, OrderService
from ..schemas import ProductDTO, CustomerDTO, AddressDTO
from ..utils import DataLoader
from ..enum import OrderStatus


class ApplicationService:
    """Main application service that initializes and coordinates all components"""

    def __init__(self):
        # Initialize repositories
        self._product_repo = ProductRepository()
        self._customer_repo = CustomerRepository()
        self._order_repo = OrderRepository()
        self._warehouse_repo = WarehouseRepository()

        # Initialize services
        self._product_service = ProductService(self._product_repo)
        self._customer_service = CustomerService(self._customer_repo)
        self._cart_service = CartService(self._product_repo)
        self._order_service = OrderService(
            self._order_repo,
            self._product_repo,
            self._customer_repo
        )
        # Initialize data loader
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "utils"

        self._data_loader = DataLoader(data_dir=data_dir)

    @property
    def product_service(self) -> ProductService:
        """Get product service instance"""
        return self._product_service

    @property
    def customer_service(self) -> CustomerService:
        """Get customer service instance"""
        return self._customer_service

    @property
    def cart_service(self) -> CartService:
        """Get cart service instance"""
        return self._cart_service

    @property
    def order_service(self) -> OrderService:
        """Get order service instance"""
        return self._order_service

    @property
    def warehouse_repo(self) -> WarehouseRepository:
        """Get warehouse repository instance"""
        return self._warehouse_repo

    def initialize_sample_data(self) -> dict:
        """Initialize the application with sample data from JSON files"""
        products_data = self._data_loader.load_products()
        customers_data = self._data_loader.load_customers()

        products = {}
        for prod_data in products_data:
            product_dto = ProductDTO(**prod_data)
            created_product = self._product_service.create_product(product_dto)
            key = prod_data['name'].lower().replace(' ', '_').split('_')[0]
            products[key] = created_product

        customers = {}
        for cust_data in customers_data:
            addresses = [AddressDTO(**addr) for addr in cust_data['addresses']]
            customer_dto = CustomerDTO(
                id=cust_data['id'],
                name=cust_data['name'],
                email=cust_data['email'],
                addresses=addresses
            )
            created_customer = self._customer_service.create_customer(customer_dto)
            key = cust_data['name'].split()[0].lower()
            customers[key] = created_customer

        return {
            'products': products,
            'customers': customers
        }

    def get_statistics(self) -> dict:
        """Get application statistics"""
        all_products = self._product_service.get_all_products()
        all_customers = self._customer_service.get_all_customers()
        all_orders = self._order_service.get_all_orders()

        total_revenue = sum(order.total_amount for order in all_orders)
        active_orders = [order for order in all_orders if order.status != OrderStatus.CANCELLED]
        cancelled_orders = [order for order in all_orders if order.status == OrderStatus.CANCELLED]

        return {
            'total_products': len(all_products),
            'total_customers': len(all_customers),
            'total_orders': len(all_orders),
            'active_orders': len(active_orders),
            'cancelled_orders': len(cancelled_orders),
            'total_revenue': total_revenue
        }

    def reset(self):
        """Reset all data (useful for testing)"""
        self._product_repo = ProductRepository()
        self._customer_repo = CustomerRepository()
        self._order_repo = OrderRepository()
        self._warehouse_repo = WarehouseRepository()

        self._product_service = ProductService(self._product_repo)
        self._customer_service = CustomerService(self._customer_repo)
        self._cart_service = CartService(self._product_repo)
        self._order_service = OrderService(
            self._order_repo,
            self._product_repo,
            self._customer_repo
        )
