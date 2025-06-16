from sqlalchemy import Column, Integer, String, Float
from database.base import Base
from sqlalchemy.orm import (
    Mapped,
    relationship
)
from .realty_table import RealtyTable
from .user_table import UserTable
from database.associates import apartment_assoc_table, apartment_user_assoc_table


class ApartmentsTable(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    street = Column(String)
    floor = Column(Integer)
    rooms = Column(Integer)
    area = Column(Float)
    price = Column(Float)

    type: Mapped[RealtyTable] = relationship(secondary=apartment_assoc_table)

    user: Mapped[UserTable] = relationship(secondary=apartment_user_assoc_table)
