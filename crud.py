from sqlalchemy.orm import Session, joinedload
import models, schemas
from fastapi import HTTPException

# =======================
# AUTHOR OPERATIONS
# =======================

# 1. Get a single author by ID
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

# 2. Get a single author by Email (used to check duplicates)
def get_author_by_email(db: Session, email: str):
    return db.query(models.Author).filter(models.Author.email == email).first()

# 3. Get a list of all authors
def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

# 4. Create a new author
def create_author(db: Session, author: schemas.AuthorCreate):
    # Check if email already exists
    db_author = get_author_by_email(db, author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the actual database object
    new_author = models.Author(name=author.name, email=author.email)
    db.add(new_author)
    db.commit()      # Save to DB
    db.refresh(new_author) # Reload data to get the new ID
    return new_author

# 5. Delete an author
def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if not db_author:
        return False
    db.delete(db_author)
    db.commit()
    return True

# 6. Update an author
def update_author(db: Session, author_id: int, author_data: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    db_author.name = author_data.name
    db_author.email = author_data.email
    db.commit()
    db.refresh(db_author)
    return db_author


# =======================
# POST OPERATIONS
# =======================

# 1. Create a Post
def create_post(db: Session, post: schemas.PostCreate):
    # CRITICAL REQUIREMENT: Check if author exists first!
    author = get_author(db, post.author_id)
    if not author:
        # If no author, stop immediately and return Error 400
        raise HTTPException(status_code=400, detail="Author ID does not exist")

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 2. Get all posts (with filtering)
def get_posts(db: Session, author_id: int = None):
    query = db.query(models.Post)
    
    # If author_id is provided, filter by it
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    # CRITICAL REQUIREMENT: Avoid N+1 Problem
    # joinedload loads the Author data in the SAME query as the Post
    return query.options(joinedload(models.Post.author)).all()

# 3. Get single post
def get_post(db: Session, post_id: int):
    # Also uses joinedload to get author details
    return db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == post_id).first()

# 4. Delete post
def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return False
    db.delete(db_post)
    db.commit()
    return True

# 5. Update post
def update_post(db: Session, post_id: int, post_data: schemas.PostBase):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    db_post.title = post_data.title
    db_post.content = post_data.content
    db.commit()
    db.refresh(db_post)
    return db_post

# 6. Helper for "GET /authors/{id}/posts"
def get_posts_by_author_id(db: Session, author_id: int):
    return db.query(models.Post).filter(models.Post.author_id == author_id).all()