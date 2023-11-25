# Standard library imports
import os

# Related third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI

# Local application/library specific imports
# Database configuration
from app.database.database import SessionLocal, engine

# Database seeder
from app.database.database_seeder import seed_data

# ORM models
from app.models.baseball_player_score import BaseballPlayerScore

# API routers
from app.routers import baseball_scores_router

load_dotenv()

app = FastAPI()

# Include routers.
app.include_router(baseball_scores_router.router)


@app.on_event("startup")
def on_startup():
    # Create database tables
    BaseballPlayerScore.metadata.create_all(bind=engine)
    print("RUN_SEEDER:", os.getenv('RUN_SEEDER', 'false').lower())
    if os.getenv('RUN_SEEDER', 'false').lower() == 'true':
        db = SessionLocal()
        try:
            # Check if any data exists
            if db.query(BaseballPlayerScore).first() is None:
                seed_data(db)
        finally:
            db.close()
