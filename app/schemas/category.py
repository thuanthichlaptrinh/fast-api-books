from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None # des có thể có hoặc không

class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    pass

class CategoryUpdate(BaseModel):
    """Schema for updating an existing category"""
    name: str | None = None
    description: str | None = None

class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True # Pydantic read from SQLAlchemy model instances

class Category(CategoryInDBBase):
    """Schema return for client"""
    pass