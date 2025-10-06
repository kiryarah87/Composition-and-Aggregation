class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
    ):
        self.product_id = product_id
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value


class Category:
    def __init__(self, name: str):
        self.name = name
        self._products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return self._products

    def add_product(self, product: Product):
        if product not in self._products:
            self._products.append(product)

    def remove_product(self, product: Product):
        if product in self._products:
            self._products.remove(product)
