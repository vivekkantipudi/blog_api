from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import engine, get_db

# CRITICAL STEP: Create the Database Tables
# This line looks at models.py and creates the actual tables in MySQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API Platform")

# =======================
# AUTHOR ENDPOINTS
# =======================

@app.post("/authors", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors", response_model=List[schemas.AuthorResponse])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@app.get("/authors/{id}", response_model=schemas.AuthorResponse)
def read_author(id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.put("/authors/{id}", response_model=schemas.AuthorResponse)
def update_author(id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.delete("/authors/{id}")
def delete_author(id: int, db: Session = Depends(get_db)):
    success = crud.delete_author(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Author and associated posts deleted"}

# NESTED ENDPOINT: Get posts for a specific author
@app.get("/authors/{id}/posts", response_model=List[schemas.PostResponse])
def read_author_posts(id: int, db: Session = Depends(get_db)):
    # First, check if the author exists
    if not crud.get_author(db, id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_posts_by_author_id(db, id)


# =======================
# POST ENDPOINTS
# =======================

@app.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Note: crud.create_post already handles the 400 error if author is missing
    return crud.create_post(db=db, post=post)

@app.get("/posts", response_model=List[schemas.PostResponse])
def read_posts(author_id: int = Query(None), db: Session = Depends(get_db)):
    # This handles the filter requirement: GET /posts?author_id=123
    return crud.get_posts(db, author_id)

@app.get("/posts/{id}", response_model=schemas.PostWithAuthor)
def read_post(id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    success = crud.delete_post(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}