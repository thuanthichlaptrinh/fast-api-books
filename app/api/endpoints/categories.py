from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import category_service


router = APIRouter()


@router.get("/", response_model=List[Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of categories with pagination"""
    return category_service.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a category by its ID"""
    return category_service.get_category(db, category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    return category_service.create_category(db, category)


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Update an existing category"""
    return category_service.update_category(db, category_id, category)


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    return category_service.delete_category(db, category_id)


@router.get("/search/", response_model=List[Category])
def search_categories(keyword: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search categories by name keyword"""
    return category_service.search_categories(db, keyword, skip=skip, limit=limit)
