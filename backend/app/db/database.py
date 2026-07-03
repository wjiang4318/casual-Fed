'''
This file is used to set up the connection to Supabase

SQLALchemy needs two things to talk to postgres
1. Engine — the actual connection to your database (uses your DATABASE_URL)
2. Session — a workspace for one unit of work (read/write operations)
(phone line to the database vs one phone call)
'''

# run this file only manually to create the tables in supabase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.db.models import Base

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# phone line to the database - every query goes through this 
engine = create_engine(DATABASE_URL)

# factory that creates sessions (one session = one phone call/unit of work)
SessionLocal = sessionmaker(bind=engine)

# only runs when this file is executed directly, not when imported by other files
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Connection successful!")
        # reads all model classes (Meeting, etc.) and creates their tables in Postgres if they don't exist
        Base.metadata.create_all(engine)
        print("Tables created!")
    except Exception as e:
        print(f"Failed: {e}")
