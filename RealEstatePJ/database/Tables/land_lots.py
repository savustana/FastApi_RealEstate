from sqlalchemy import Column, Integer, String, Float
from database.base import Base
from sqlalchemy.orm import (
    Mapped,
    relationship
)
from .realty_table import RealtyTable
from .user_table import UserTable
from database.associates import land_lots_assoc_table, land_lots_user_assoc_table


class LandLotsTable(Base):
    __tablename__ = "land_lots"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    street = Column(String)
    area = Column(Float)
    price = Column(Float)

    type: Mapped[RealtyTable] = relationship(secondary=land_lots_assoc_table)

    user: Mapped[UserTable] = relationship(secondary=land_lots_user_assoc_table)
