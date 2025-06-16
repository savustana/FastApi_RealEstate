from sqlalchemy.orm import Session
from database.schema import User
from database.schema import Realty, Apartments, TemporaryHouse, LandLots
from database.Tables.user_table import UserTable
from database.Tables.realty_table import RealtyTable
from database.Tables.temporary_house import TempHouseTable
from database.Tables.apartments_table import ApartmentsTable
from database.Tables.land_lots import LandLotsTable
import bcrypt
from werkzeug.security import generate_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(UserTable).filter(email == UserTable.email).first()


def get_realty_apartment(db: Session):
    return db.query(ApartmentsTable).all()


def get_realty_temp_house(db: Session):
    return db.query(TempHouseTable).all()


def get_realty_land_lot(db: Session):
    return db.query(LandLotsTable).all()


def create_user(db: Session, user: User):
    pwdhash = generate_password_hash(user.password)

    username = user.email.split('@')[0]
    db_user = UserTable(email=user.email,
                        username=username,
                        hashed_password=pwdhash,
                        start_connection=user.start_connect)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_realty_type(db: Session, realty: Realty):

    db_realty = RealtyTable(type_of_estate=realty.type_of_estate)
    db.add(db_realty)
    db.commit()
    db.refresh(db_realty)
    return db_realty


def create_realty_temp_house(db: Session, realty: TemporaryHouse, token: str):
    realty_type = db.query(RealtyTable).filter(1 == RealtyTable.id).first()
    user = get_user_by_email(db, token)
    db_realty = TempHouseTable(city=realty.city,
                               street=realty.street,
                               land_area=realty.land_area,
                               house_area=realty.house_area,
                               floor=realty.floor,
                               price=realty.price,
                               type=realty_type,
                               user=user,)
    db.add(db_realty)
    db.commit()
    db.refresh(db_realty)
    return db_realty


def create_realty_apartment(db: Session, realty: Apartments, token: str):
    realty_type = db.query(RealtyTable).filter(2 == RealtyTable.id).first()
    user = get_user_by_email(db, token)
    db_realty = ApartmentsTable(city=realty.city,
                                street=realty.street,
                                area=realty.area,
                                floor=realty.floor,
                                rooms=realty.rooms,
                                price=realty.price,
                                type=realty_type,
                                user=user,)
    db.add(db_realty)
    db.commit()
    db.refresh(db_realty)
    return db_realty


def create_realty_land_lot(db: Session, realty: LandLots, token: str):
    realty_type = db.query(RealtyTable).filter(3 == RealtyTable.id).first()
    user = get_user_by_email(db, token)
    db_realty = LandLotsTable(city=realty.city,
                              street=realty.street,
                              area=realty.area,
                              price=realty.price,
                              type=realty_type,
                              user=user)
    db.add(db_realty)
    db.commit()
    db.refresh(db_realty)
    return db_realty
