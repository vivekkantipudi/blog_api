from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Author(Base):
    # This defines the table name in MySQL
    __tablename__ = "authors"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # unique=True ensures no two authors have the same email
    email = Column(String(100), unique=True, index=True, nullable=False)

    # RELATIONSHIP LINK:
    # This tells SQLAlchemy: "I have a relationship with the Post table."
    # cascade="all, delete-orphan" IS THE CRITICAL REQUIREMENT.
    # It means: If I delete this Author, delete all their Posts automatically.
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # FOREIGN KEY:
    # This links the post to a specific author ID.
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # RELATIONSHIP LINK:
    # This allows us to access the author info from a post object (e.g., my_post.author.name)
    author = relationship("Author", back_populates="posts")