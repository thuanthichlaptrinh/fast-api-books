from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.author_repository import author_repository
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    """Service layer for Author business logic"""
    
    def __init__(self):
        self.repository = author_repository
    
    def get_author(self, db: Session, author_id: int):
        """Get a single author by ID"""
        author = self.repository.get_by_id(db, author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        return author
    
    def get_authors(self, db: Session, skip: int = 0, limit: int = 100):
        """Get all authors with pagination"""
        return self.repository.get_all(db, skip=skip, limit=limit, order_by="name")
    
    def create_author(self, db: Session, author_in: AuthorCreate):
        """Create a new author"""
        # Check if name already exists
        existing_author = self.repository.get_by_name(db, author_in.name)
        if existing_author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Author with name '{author_in.name}' already exists"
            )
        
        # Create author
        author_data = author_in.model_dump()
        return self.repository.create(db, author_data)
    
    def update_author(self, db: Session, author_id: int, author_in: AuthorUpdate):
        """Update an author"""
        # Check if author exists
        existing_author = self.repository.get_by_id(db, author_id)
        if not existing_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if author_in.name and author_in.name != existing_author.name:
            name_exists = self.repository.get_by_name(db, author_in.name)
            if name_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Author with name '{author_in.name}' already exists"
                )
        
        # Update only provided fields
        update_data = author_in.model_dump(exclude_unset=True)
        return self.repository.update(db, author_id, update_data)
    
    def delete_author(self, db: Session, author_id: int):
        """Delete an author"""
        success = self.repository.delete(db, author_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        return {"message": "Author deleted successfully"}
    
    def search_authors(self, db: Session, keyword: str, skip: int = 0, limit: int = 100):
        """Search authors by name keyword"""
        return self.repository.search_by_name(db, keyword, skip=skip, limit=limit)


author_service = AuthorService()
