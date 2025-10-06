from ..repositories import ProductRepository
from ..schemas import ProductDTO


class ProductService:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def create_product(self, dto: ProductDTO) -> ProductDTO:
        """Create a new product and add it to the repository."""
        if dto.price < 0:
            raise ValueError("Price cannot be negative")

        product = self._repository.create(dto.product_id, dto.name, dto.price)
        return ProductDTO.from_model(product)

    def get_product(self, product_id: int) -> ProductDTO | None:
        """Retrieve a product by its ID."""
        product = self._repository.get_by_id(product_id)
        return ProductDTO.from_model(product) if product else None

    def update_price(self, product_id: int, new_price: float) -> None:
        """Update the price of an existing product."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")

        product = self._repository.get_by_id(product_id)

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        product.price = new_price
        self._repository.update(product)

    def get_all_products(self) -> list[ProductDTO]:
        """Retrieve all products from the repository."""
        products = self._repository.get_all()
        return [ProductDTO.from_model(p) for p in products]

    def delete_product(self, product_id: int) -> None:
        """Delete a product from the repository."""
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        self._repository.delete(product_id)
