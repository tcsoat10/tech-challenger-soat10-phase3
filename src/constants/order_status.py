from enum import Enum

class OrderStatusEnum(Enum):
    ORDER_PLACED = ("order_placed", "The customer has placed the order.")
    ORDER_PREPARING = ("order_preparing", "The order is being prepared.")
    ORDER_READY = ("order_ready", "The order is ready for pickup at the counter.")
    ORDER_COMPLETED = ("order_completed", "The customer has received the order.")
    ORDER_CANCELLED = ("order_cancelled", "The order was cancelled by the customer or staff.")

    @property
    def status(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def values_and_descriptions(cls):
        return [{"status": member.status, "description": member.description} for member in cls]
