import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyInteger
from faker import Faker

from src.core.domain.entities.order_item import OrderItem
from tests.factories.product_factory import ProductFactory

fake = Faker()

class OrderItemFactory(SQLAlchemyModelFactory):
 
    class Meta:
        model = OrderItem
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    
    # TODO: add reference to order
    # order_id = factory.Sequence(lambda n: n + 1) # TODO: replace with order factory
    
    product = factory.SubFactory(ProductFactory)
    product_id = factory.SelfAttribute("product.id")
    quantity = FuzzyInteger(1, 10)
    observation = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
