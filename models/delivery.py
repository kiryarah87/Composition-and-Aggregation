from abc import ABC, abstractmethod


class Delivery(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass


class StandardDelivery(Delivery):
    def cost(self) -> float:
        return 5.0


class ExpressDelivery(Delivery):
    def cost(self) -> float:
        return 15.0
