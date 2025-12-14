from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.category import Category


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model"""
    
    def __init__(self):
        super().__init__(Category)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """Get category by name"""
        return db.query(Category).filter(Category.name == name).first()
    
    def search_by_name(self, db: Session, keyword: str, skip: int = 0, limit: int = 100):
        """Search categories by name keyword"""
        return db.query(Category).filter(Category.name.ilike(f"%{keyword}%")).offset(skip).limit(limit).all()


category_repository = CategoryRepository()
