from sqlalchemy import Column, Integer, String, Float
from database.base import Base
from sqlalchemy.orm import (
    Mapped,
    relationship
)
from .realty_table import RealtyTable
from .user_table import UserTable
from database.associates import temp_house_assoc_table, temp_house_user_assoc_table


class TempHouseTable(Base):
    __tablename__ = "temporary_house"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    street = Column(String)
    land_area = Column(Float)
    house_area = Column(Float)
    floor = Column(Integer)
    price = Column(Float)

    type: Mapped[RealtyTable] = relationship(secondary=temp_house_assoc_table)

    user: Mapped[UserTable] = relationship(secondary=temp_house_user_assoc_table)
