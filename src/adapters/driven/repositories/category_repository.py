from typing import List
from sqlalchemy.sql import exists
from src.adapters.driven.repositories.models.category_model import CategoryModel
from src.core.domain.entities.category import Category
from src.core.ports.category.i_category_repository import ICategoryRepository
from sqlalchemy.orm import Session

class CategoryRepository(ICategoryRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, category: Category) -> Category:
        category_model: CategoryModel = CategoryModel.from_entity(category)
        self.db_session.add(category_model)
        self.db_session.commit()
        self.db_session.refresh(category_model)
        return category_model.to_entity()

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(CategoryModel.name == name)).scalar()

    def get_by_name(self, name: str) -> Category:
        category_model = self.db_session.query(CategoryModel).filter(CategoryModel.name == name).first()
        if category_model is None:
            return None
        return category_model.to_entity()

    def get_by_id(self, category_id: int) -> Category:
        category_model = self.db_session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if category_model is None:
            return None
        return category_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[Category]:
        query = self.db_session.query(CategoryModel)
        if not include_deleted:
            query = query.filter(CategoryModel.inactivated_at.is_(None))
        categories_models = query.all()
        return [category_model.to_entity() for category_model in categories_models]

    def update(self, category: Category) -> Category:
        category_model = CategoryModel.from_entity(category)
        self.db_session.merge(category_model)
        self.db_session.commit()
        return category_model.to_entity()

    def delete(self, category: Category) -> None:
        category_model = self.db_session.query(CategoryModel).filter(CategoryModel.id == category.id).first()
        self.db_session.delete(category_model)
        self.db_session.commit()
