from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service layer for Category business logic"""
    
    def __init__(self):
        self.repository = category_repository
    
    def get_category(self, db: Session, category_id: int):
        """Get a single category by ID"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return category
    
    def get_categories(self, db: Session, skip: int = 0, limit: int = 100):
        """Get all categories with pagination"""
        return self.repository.get_all(db, skip=skip, limit=limit, order_by="name")
    
    def create_category(self, db: Session, category_in: CategoryCreate):
        """Create a new category"""
        # Check if name already exists
        existing_category = self.repository.get_by_name(db, category_in.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_in.name}' already exists"
            )
        
        # Create category
        category_data = category_in.model_dump()
        return self.repository.create(db, category_data)
    
    def update_category(self, db: Session, category_id: int, category_in: CategoryUpdate):
        """Update a category"""
        # Check if category exists
        existing_category = self.repository.get_by_id(db, category_id)
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if category_in.name and category_in.name != existing_category.name:
            name_exists = self.repository.get_by_name(db, category_in.name)
            if name_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with name '{category_in.name}' already exists"
                )
        
        # Update only provided fields
        update_data = category_in.model_dump(exclude_unset=True)
        return self.repository.update(db, category_id, update_data)
    
    def delete_category(self, db: Session, category_id: int):
        """Delete a category"""
        success = self.repository.delete(db, category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return {"message": "Category deleted successfully"}
    
    def search_categories(self, db: Session, keyword: str, skip: int = 0, limit: int = 100):
        """Search categories by name keyword"""
        return self.repository.search_by_name(db, keyword, skip=skip, limit=limit)


category_service = CategoryService()
