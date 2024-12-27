from sqlalchemy.sql import exists
from src.core.domain.entities.category import Category
from src.core.ports.category.i_categorory_repository import ICategoryRepository
from sqlalchemy.orm import Session

class CategoryRepository(ICategoryRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, category: Category) -> Category:
        self.db_session.add(category)
        self.db_session.commit()
        self.db_session.refresh(category)
        return category

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Category.name == name)).scalar()

    def get_by_name(self, name: str) -> Category:
        return self.db_session.query(Category).filter(Category.name == name).first()

    def get_by_id(self, category_id: int) -> Category:
        return self.db_session.query(Category).filter(Category.id == category_id).first()

    def get_all(self) -> Category:
        return self.db_session.query(Category).all()

    def update(self, category: Category) -> Category:
        self.db_session.merge(category)
        self.db_session.commit()
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        if category:
            self.db_session.delete(category)
            self.db_session.commit()
