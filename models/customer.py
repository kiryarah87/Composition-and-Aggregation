class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.addresses: list[Address] = []

    def add_address(self, street: str, city: str, country: str):
        self.addresses.append(Address(street, city, country))


class Address:
    def __init__(self, street: str, city: str, country: str):
        self.street = street
        self.city = city
        self.country = country
