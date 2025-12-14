from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.book import Book


class BookRepository(BaseRepository[Book]):
    """Repository for Book model"""
    
    def __init__(self):
        super().__init__(Book)
    
    def get_by_title(self, db: Session, title: str) -> Optional[Book]:
        """Get book by title"""
        return db.query(Book).filter(Book.title == title).first()
    
    def get_by_author(self, db: Session, author_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get books by author ID"""
        return db.query(Book).filter(Book.author_id == author_id).offset(skip).limit(limit).all()
    
    def get_by_category(self, db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get books by category ID"""
        return db.query(Book).filter(Book.category_id == category_id).offset(skip).limit(limit).all()
    
    def search_by_title(self, db: Session, keyword: str, skip: int = 0, limit: int = 100) -> List[Book]:
        """Search books by title keyword"""
        return db.query(Book).filter(Book.title.ilike(f"%{keyword}%")).offset(skip).limit(limit).all()


book_repository = BookRepository()
