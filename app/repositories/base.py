from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base Repository with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "id",
        desc_order: bool = False
    ) -> List[ModelType]:
        """Get all records with pagination"""
        query = db.query(self.model)
        
        if hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            if desc_order:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(order_column)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        id: int, 
        obj_in: Dict[str, Any]
    ) -> Optional[ModelType]:
        """Update a record"""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Delete a record"""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return False
        
        db.delete(db_obj)
        db.commit()
        return True
    
    def count(self, db: Session) -> int:
        """Count total records"""
        return db.query(self.model).count()
