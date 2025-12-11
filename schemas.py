from pydantic import BaseModel, EmailStr
from typing import List, Optional



# This is the base shape (shared data)
class AuthorBase(BaseModel):
    name: str
    email: EmailStr  # This automatically checks if it's a valid email format!

# We use this when CREATING an author (User sends this)
class AuthorCreate(AuthorBase):
    pass

# We use this when RESPONDING to the user (API sends this)
class AuthorResponse(AuthorBase):
    id: int  # The database creates the ID, so it's only in the response
    
    class Config:
        from_attributes = True # This tells Pydantic to read data from our SQL Models


class PostBase(BaseModel):
    title: str
    content: str

# When creating a post, we need the Author's ID
class PostCreate(PostBase):
    author_id: int

# Standard response for a post
class PostResponse(PostBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class PostWithAuthor(PostResponse):
    author: AuthorResponse