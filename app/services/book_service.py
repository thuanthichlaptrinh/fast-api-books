from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
import os

from app.repositories.book_repository import book_repository
from app.schemas.book import BookCreate, BookUpdate
from app.core.utils import save_upload_file, delete_file, get_file_path_from_url


class BookService:
    """Service layer for Book business logic"""
    
    def __init__(self):
        self.repository = book_repository
    
    def get_book(self, db: Session, book_id: int):
        """Get a single book by ID"""
        book = self.repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
        return book
    
    def get_books(self, db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None, category_id: Optional[int] = None, year: Optional[int] = None, keyword: Optional[str] = None):
        """Get all books with pagination"""
        return self.repository.get_all(
            db, 
            skip=skip, 
            limit=limit, 
            filters={"author_id": author_id, "category_id": category_id, "year": year, "keyword": keyword}, 
            order_by=[("created_at", "desc")]
        )
    
    def create_book(self, db: Session, book_in: BookCreate):
        """Create a new book"""
        # Check if title already exists
        existing_book = self.repository.get_by_title(db, book_in.title)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with title '{book_in.title}' already exists"
            )
        
        # Create book
        book_data = book_in.model_dump()
        return self.repository.create(db, book_data)
    
    def update_book(self, db: Session, book_id: int, book_in: BookUpdate):
        """Update a book"""
        # Check if book exists
        existing_book = self.repository.get_by_id(db, book_id)
        if not existing_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        
        # Check if new title already exists (if title is being updated)
        if book_in.title and book_in.title != existing_book.title:
            title_exists = self.repository.get_by_title(db, book_in.title)
            if title_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with title '{book_in.title}' already exists"
                )
        
        # Update only provided fields
        update_data = book_in.model_dump(exclude_unset=True)
        return self.repository.update(db, book_id, update_data)
    
    def delete_book(self, db: Session, book_id: int):
        """Delete a book"""
        success = self.repository.delete(db, book_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return {"message": "Book deleted successfully"}
    
    def get_books_by_author(self, db: Session, author_id: int, skip: int = 0, limit: int = 100):
        """Get all books by a specific author"""
        return self.repository.get_by_author(db, author_id, skip=skip, limit=limit)
    
    def get_books_by_category(self, db: Session, category_id: int, skip: int = 0, limit: int = 100):
        """Get all books by a specific category"""
        return self.repository.get_by_category(db, category_id, skip=skip, limit=limit)
    
    def search_books(self, db: Session, keyword: str, skip: int = 0, limit: int = 100):
        """Search books by title keyword"""
        return self.repository.search_by_title(db, keyword, skip=skip, limit=limit)
    
    async def upload_cover_image(self, db: Session, book_id: int, file: UploadFile):
        """
        Upload cover image for a book
        
        Args:
            db: Database session
            book_id: ID of the book
            file: Uploaded image file
            
        Returns:
            Updated book with new cover image URL
        """
        # Check if book exists
        book = self.repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        
        # Delete old cover image if exists
        if book.cover_image:
            old_file_path = get_file_path_from_url(book.cover_image)
            delete_file(old_file_path)
        
        # Save new cover image
        try:
            file_path, url_path = await save_upload_file(file)
            
            # Update book with new cover image URL
            updated_book = self.repository.update(db, book_id, {"cover_image": url_path})
            
            return updated_book
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload cover image: {str(e)}"
            )


book_service = BookService()
