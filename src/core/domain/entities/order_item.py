from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.domain.entities.category import Category
from src.core.exceptions.validation_exception import ValidationException
from src.core.domain.entities.base_entity import BaseEntity


class OrderItem(BaseEntity):
    __tablename__ = "order_items"

    # TODO: add relationship with order and make unique order_id and product_id
    # order_id = Column(ForeignKey("orders.id"), nullable=False)
    # order = relationship("Order", back_populates="items")

    product_id = Column(ForeignKey("products.id"), nullable=False)
    product = relationship("Product")

    quantity = Column(Integer, nullable=False, default=1)

    observation = Column(String(300))

    @property
    def total(self) -> float:
        """
        Calculates the total cost of this item based on the product price and quantity.

        :return: Total cost as a float.
        """
        return self.product.price * self.quantity
    
    @property
    def product_category(self) -> Category:
        """
        Retrieves the category of the associated product.

        :return: The category of the product.
        """
        return self.product.category
