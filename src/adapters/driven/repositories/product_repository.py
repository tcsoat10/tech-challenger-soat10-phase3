from typing import List
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.core.domain.entities.product import Product
from src.core.ports.product.i_product_repository import IProductRepository

class ProductRepository(IProductRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, product: Product) -> Product:
        self.db_session.add(product)
        self.db_session.commit()
        self.db_session.refresh(product)
        return product

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Product.name == name)).scalar()

    def get_by_name(self, name: str) -> Product:
        return self.db_session.query(Product).filter(Product.name == name).first()

    def get_by_id(self, product_id: int) -> Product:
        return self.db_session.query(Product).filter(Product.id == product_id).first()

    def get_all(self) -> List[Product]:
        return self.db_session.query(Product).all()

    def update(self, product: Product) -> Product:
        self.db_session.merge(product)
        self.db_session.commit()
        return product

