from sqlalchemy import Column, Integer, String, DATE
from database.base import Base


class UserTable(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    start_connection = Column(DATE)
