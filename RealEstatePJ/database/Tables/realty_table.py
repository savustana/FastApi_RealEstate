from sqlalchemy import Column, Integer, String
from database.base import Base


class RealtyTable(Base):
    __tablename__ = "realty"

    id = Column(Integer, primary_key=True)
    type_of_estate = Column(String)
