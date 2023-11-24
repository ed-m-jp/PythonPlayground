from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an in-memory SQLite database,
# need to change this later if this app becomes a real service.
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Base class for models.
Base = declarative_base()

# Session factory.
SessionLocal = sessionmaker(bind=engine)
