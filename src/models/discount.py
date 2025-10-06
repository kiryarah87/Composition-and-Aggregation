from abc import ABC, abstractmethod


class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class PercentageDiscount(Discount):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, amount: float) -> float:
        return amount * (self.percentage / 100)


class FixedDiscount(Discount):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount

    def apply(self, amount: float) -> float:
        return min(self.fixed_amount, amount)
