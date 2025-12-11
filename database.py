from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------
# CRITICAL STEP: YOU MUST EDIT THE LINE BELOW
# Format: mysql+pymysql://<username>:<password>@<host>/<database_name>
# ----------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:ViveK%402005@localhost/blog_db"

# This creates the engine (the actual connection to the DB)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates a 'Session' class. Each time we use the API, 
# we create a new SessionLocal() to talk to the DB, then close it.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class for our models (we will use this in Phase 3)
Base = declarative_base()

# This is a helper function that the API uses to grab a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()