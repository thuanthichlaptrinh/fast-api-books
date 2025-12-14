from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.author import Author, AuthorCreate, AuthorUpdate
from app.services.author_service import author_service


router = APIRouter()


@router.get("/", response_model=List[Author])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of authors with pagination"""
    return author_service.get_authors(db, skip=skip, limit=limit)


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get an author by its ID"""
    return author_service.get_author(db, author_id)


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    return author_service.create_author(db, author)


@router.put("/{author_id}", response_model=Author)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    """Update an existing author"""
    return author_service.update_author(db, author_id, author)


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author"""
    return author_service.delete_author(db, author_id)


@router.get("/search/", response_model=List[Author])
def search_authors(keyword: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search authors by name keyword"""
    return author_service.search_authors(db, keyword, skip=skip, limit=limit)

