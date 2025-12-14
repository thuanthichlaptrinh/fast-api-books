from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app import models
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get("/", response_model=List[Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list categories, pagination sample use skip/limit"""
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a category by its ID"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    new_category = db.query(models.Category).filter(models.Category.name == category.name).first()

    if new_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    category = models.Category(name=category.name, description=category.description)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category

@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    """Update an existing category"""
    existing_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not existing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if category_update.name is not None and category_update.name != existing_category.name:
        name_conflict = db.query(models.Category).filter(
            models.Category.name == category_update.name,
            models.Category.id != category_id  # Loại trừ chính nó
        ).first()

        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        else:
            existing_category.name = category_update.name

    if category_update.description is not None:
        existing_category.description = category_update.description

    db.add(existing_category)
    db.commit()
    db.refresh(existing_category)

    return existing_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete an existing category"""
    existing_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not existing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    # Kiểm tra liên kết
    linked_books = db.query(models.Book).filter(models.Book.category_id == category_id).first()
    if linked_books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with linked books"
        )

    db.delete(existing_category)
    db.commit()