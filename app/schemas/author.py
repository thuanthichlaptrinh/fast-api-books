from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None # des có thể có hoặc không

class AuthorCreate(AuthorBase):
    """Schema for creating a new author"""
    pass

class AuthorUpdate(BaseModel):
    """Schema for updating an existing author   """
    name: str | None = None
    bio: str | None = None

class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True 

class Author(AuthorInDBBase):
    """Schema return for client"""
    pass