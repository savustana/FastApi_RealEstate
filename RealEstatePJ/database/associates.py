from sqlalchemy import Table, Column, ForeignKey
from .base import Base


apartment_user_assoc_table = Table(
    'apartment_user_assoc_table',
    Base.metadata,
    Column('apartments_id',
           ForeignKey('apartments.id'),
           primary_key=True),
    Column('user_id',
           ForeignKey('user.id'),
           primary_key=True
           )
)

temp_house_user_assoc_table = Table(
    'temp_house_user_assoc_table',
    Base.metadata,
    Column('temporary_house_id',
           ForeignKey('temporary_house.id'),
           primary_key=True),
    Column('user_id',
           ForeignKey('user.id'),
           primary_key=True
           )
)

land_lots_user_assoc_table = Table(
    'land_lots_user_assoc_table',
    Base.metadata,
    Column('land_lots_id',
           ForeignKey('land_lots.id'),
           primary_key=True),
    Column('user_id',
           ForeignKey('user.id'),
           primary_key=True
           )
)


apartment_assoc_table = Table(
    'apartment_assoc_table',
    Base.metadata,
    Column('apartments_id',
           ForeignKey('apartments.id'),
           primary_key=True),
    Column('type_id',
           ForeignKey('realty.id'),
           primary_key=True),

)


land_lots_assoc_table = Table(
    'land_lots_assoc_table',
    Base.metadata,
    Column('land_lots_id',
           ForeignKey('land_lots.id'),
           primary_key=True),
    Column('type_id',
           ForeignKey('realty.id'),
           primary_key=True),

)

temp_house_assoc_table = Table(
    'temp_house_assoc_table',
    Base.metadata,
    Column('temporary_houses_id',
           ForeignKey('temporary_house.id'),
           primary_key=True),
    Column('type_id',
           ForeignKey('realty.id'),
           primary_key=True
           )
)
