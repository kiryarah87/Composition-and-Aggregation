from models.product import Product


class ProductRepository:
    def __init__(self):
        self._products: dict[int, Product] = {}

    def create(
        self,
        product_id: int,
        name: str,
        price: float
    ) -> Product:
        '''Creates a new product and adds it to the repository.'''
        product = Product(product_id, name, price)
        self.add(product)
        return product

    def add(self, product: Product) -> None:
        '''Adds a product to the repository.'''
        self._products[product.product_id] = product

    def get_by_id(self, product_id: int) -> Product | None:
        '''Retrieves a product by its ID.'''
        return self._products.get(product_id)

    def get_all(self) -> list[Product]:
        '''Retrieves all products in the repository.'''
        return list(self._products.values())

    def update(self, product: Product) -> None:
        '''Updates an existing product in the repository.'''
        if product.product_id not in self._products:
            raise ValueError(f"Product with id {product.product_id} not found")
        self._products[product.product_id] = product

    def delete(self, product_id: int) -> None:
        '''Deletes a product from the repository by its ID.'''
        if product_id not in self._products:
            raise ValueError(f"Product with id {product_id} not found")
        del self._products[product_id]
