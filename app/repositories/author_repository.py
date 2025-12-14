from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.author import Author


class AuthorRepository(BaseRepository[Author]):
    """Repository for Author model"""
    
    def __init__(self):
        super().__init__(Author)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Author]:
        """Get author by name"""
        return db.query(Author).filter(Author.name == name).first()
    
    def search_by_name(self, db: Session, keyword: str, skip: int = 0, limit: int = 100):
        """Search authors by name keyword"""
        return db.query(Author).filter(Author.name.ilike(f"%{keyword}%")).offset(skip).limit(limit).all()


author_repository = AuthorRepository()
