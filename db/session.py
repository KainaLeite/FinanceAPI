from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(
    database_url
)

SessioLocal = sessionmaker(
    autocommit = False, 
    autoflush = False,
    bind=engine
)

def get_db():
    try:
        db = SessioLocal()    
        yield db                    
    finally:
        db.close()