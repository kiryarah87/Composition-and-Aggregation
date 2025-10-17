from ..models import Warehouse, Product


class WarehouseRepository:
    def __init__(self):
        self._warehouse = Warehouse()

    def add_stock(self, product: Product, quantity: int) -> None:
        self._warehouse.add_stock(product, quantity)

    def remove_stock(self, product: Product, quantity: int) -> None:
        self._warehouse.remove_stock(product, quantity)

    def get_stock(self, product: Product) -> int:
        return self._warehouse.stock.get(product, 0)

    def check_availability(self, product: Product, quantity: int) -> bool:
        return self.get_stock(product) >= quantity
