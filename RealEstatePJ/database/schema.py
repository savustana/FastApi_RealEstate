from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class User(BaseModel):
    username: str = Field(..., min_length=1, description="your username")
    email: EmailStr = Field(..., min_length=1, description="your email")
    password: str = Field(..., min_length=6, description="your password")
    start_connect: datetime = Field(datetime.now(), description="your connection time")


class Realty(BaseModel):
    type_of_estate: str = Field(..., min_length=1, description="Ex: detached house/apt/land lot")


class RealtyAbstract(BaseModel):
    city: str = Field(..., min_length=1, description="City")
    street: str = Field(..., min_length=1, description="Street")
    price: float = Field(..., le=0, description="Price")


class Apartments(RealtyAbstract):
    area: float = Field(..., description="Area")
    floor: int = Field(..., le=0, description="Floor")
    rooms: int = Field(..., le=0, description="Rooms")


class LandLots(RealtyAbstract):
    area: float = Field(..., description="Area")


class TemporaryHouse(RealtyAbstract):
    land_area: float = Field(..., le=0, description="Land area")
    house_area: float = Field(..., le=0, description="House area")
    floor: int = Field(..., le=0, description="Floor")
