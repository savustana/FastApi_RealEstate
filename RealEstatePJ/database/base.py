from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

schema_db = "sqlite:///database.db"

engine = create_engine(schema_db,
                       connect_args={"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
