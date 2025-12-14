from typing import Generic, TypeVar, Type, Optional, List, Any, Dict, Callable
from sqlalchemy.orm import Session, Query
from sqlalchemy import desc, asc

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base Repository with flexible CRUD operations
    
    Provides a flexible query builder pattern that allows:
    - Dynamic filtering
    - Multiple sorting options
    - Pagination
    - Custom query modifications
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_query(self, db: Session) -> Query:
        """Get base query for the model"""
        return db.query(self.model)
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        return self.get_query(db).filter(self.model.id == id).first()
    
    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[tuple]] = None,
        query_modifier: Optional[Callable[[Query], Query]] = None
    ) -> List[ModelType]:
        """
        Get all records with flexible filtering and pagination
        
        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            filters: Dict of field-value pairs for filtering (e.g., {'author_id': 1})
            order_by: List of tuples (field_name, direction) for sorting 
                     e.g., [('created_at', 'desc'), ('title', 'asc')]
            query_modifier: Optional function to further modify the query
        
        Returns:
            List of model instances
        
        Example:
            # Simple pagination
            books = repo.get_all(db, skip=0, limit=10)
            
            # With filters
            books = repo.get_all(db, filters={'author_id': 1, 'published_year': 2020})
            
            # With sorting
            books = repo.get_all(db, order_by=[('created_at', 'desc'), ('title', 'asc')])
            
            # With custom query modifier
            def add_joins(query):
                return query.join(Author).filter(Author.name.like('%John%'))
            books = repo.get_all(db, query_modifier=add_joins)
        """
        query = self.get_query(db)
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)
        
        # Apply custom query modifications
        if query_modifier:
            query = query_modifier(query)
        
        # Apply ordering
        if order_by:
            for field_name, direction in order_by:
                if hasattr(self.model, field_name):
                    field = getattr(self.model, field_name)
                    if direction.lower() == 'desc':
                        query = query.order_by(desc(field))
                    else:
                        query = query.order_by(asc(field))
        
        # Apply pagination
        return query.offset(skip).limit(limit).all()
    
    def get_one(
        self,
        db: Session,
        filters: Optional[Dict[str, Any]] = None,
        query_modifier: Optional[Callable[[Query], Query]] = None
    ) -> Optional[ModelType]:
        """
        Get a single record with flexible filtering
        
        Args:
            db: Database session
            filters: Dict of field-value pairs for filtering
            query_modifier: Optional function to modify the query
        
        Returns:
            Model instance or None
        """
        query = self.get_query(db)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)
        
        if query_modifier:
            query = query_modifier(query)
        
        return query.first()
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
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
    
    def count(
        self, 
        db: Session,
        filters: Optional[Dict[str, Any]] = None,
        query_modifier: Optional[Callable[[Query], Query]] = None
    ) -> int:
        """
        Count records with optional filtering
        
        Args:
            db: Database session
            filters: Dict of field-value pairs for filtering
            query_modifier: Optional function to modify the query
        
        Returns:
            Count of records
        """
        query = self.get_query(db)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)
        
        if query_modifier:
            query = query_modifier(query)
        
        return query.count()

