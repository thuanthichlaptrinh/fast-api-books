from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import book_service

router = APIRouter()

@router.get("/", response_model=List[Book])
def list_books(
    skip: int = 0, 
    limit: int = 100, 
    author_id: int | None = None,
    category_id: int | None = None,
    year: int | None = None,
    keyword: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Get list of books with pagination
    - author_id: Filter by author ID
    - category_id: Filter by category ID
    - year: Filter by published year
    - keyword: Search by title keyword 
    """
    return book_service.get_books(db, skip=skip, limit=limit, author_id=author_id, category_id=category_id, year=year, keyword=keyword)

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a book by its ID"""
    return book_service.get_book(db, book_id)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    return book_service.create_book(db, book)

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Update an existing book"""
    return book_service.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    return book_service.delete_book(db, book_id)

@router.get("/author/{author_id}", response_model=List[Book])
def get_books_by_author(author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all books by a specific author"""
    return book_service.get_books_by_author(db, author_id, skip=skip, limit=limit)

@router.get("/category/{category_id}", response_model=List[Book])
def get_books_by_category(category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all books by a specific category"""
    return book_service.get_books_by_category(db, category_id, skip=skip, limit=limit)

@router.get("/search/", response_model=List[Book])
def search_books(keyword: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search books by title keyword"""
    return book_service.search_books(db, keyword, skip=skip, limit=limit)
