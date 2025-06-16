from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database.base import engine
from database import crud, schema
from database.Tables import user_table, apartments_table, land_lots, temporary_house
from database.base import session
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from typing import List, Annotated
import json
import jwt
import os

app = FastAPI()

user_table.Base.metadata.create_all(bind=engine)
apartments_table.Base.metadata.create_all(bind=engine)
land_lots.Base.metadata.create_all(bind=engine)
temporary_house.Base.metadata.create_all(bind=engine)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = os.getenv("SECRET_KEY", "default key")


active_connection: List[WebSocket] = []


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class Dict2Class(object):

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def jwt_verification(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# TOKEN
@app.post("/token", summary="Get token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = crud.get_user_by_email(db, email=form_data.username)
    password_db = check_password_hash(user_db.hashed_password, form_data.password)
    if user_db and password_db:
        email_token = user_db.email
        return {"access_token": email_token, "token_type": "bearer"}
    return {"message": "Incorrect username or password"}, status.HTTP_404_NOT_FOUND


@app.post("/users/")
def create_user(user: schema.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# ADD REALTY
@app.post("/realty/")
def create_realty_type(realty: schema.Realty, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    user_db_token = crud.get_user_by_email(db, email=token)
    if token != user_db_token.email:
        raise HTTPException(status_code=400, detail="Token missing")
    return crud.create_realty_type(db=db, realty=realty)


@app.post("/add-realty-temp-house/")
def create_realty_temp_house(realty: schema.TemporaryHouse, db: Session = Depends(get_db),
                             token: str = Depends(oauth2_schema)):
    user_db_token = crud.get_user_by_email(db, email=token)
    if token != user_db_token.email:
        raise HTTPException(status_code=400, detail="Token missing")

    return crud.create_realty_temp_house(db=db, realty=realty, token=token)


@app.post("/add-realty-apartment/")
def create_realty_apartment(realty: schema.Apartments, db: Session = Depends(get_db),
                            token: str = Depends(oauth2_schema)):
    user_db_token = crud.get_user_by_email(db, email=token)
    if token != user_db_token.email:
        raise HTTPException(status_code=400, detail="Token missing")

    return crud.create_realty_apartment(db=db, realty=realty, token=token)


@app.post("/add-realty-land-lot/")
def create_realty_land_lot(realty: schema.LandLots, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    user_db_token = crud.get_user_by_email(db, email=token)
    if token != user_db_token.email:
        raise HTTPException(status_code=400, detail="Token missing")
    return crud.create_realty_land_lot(db=db, realty=realty, token=token)


# SHOW REALTY
@app.get("/show-realty-temp-house")
def show_realty_temp_house(db: Session = Depends(get_db)):
    temp_house = crud.get_realty_temp_house(db=db)
    if temp_house is None:
        raise HTTPException(status_code=500, detail="Missing database")
    return temp_house


@app.get("/show-realty-apartment")
def show_realty_apartment(db: Session = Depends(get_db)):
    apartment = crud.get_realty_apartment(db=db)
    if apartment is None:
        raise HTTPException(status_code=500, detail="Missing database")
    return apartment


@app.get("/show-realty-land-lot")
def show_realty_land_lot(db: Session = Depends(get_db)):
    land_lot = crud.get_realty_land_lot(db=db)
    if land_lot is None:
        raise HTTPException(status_code=500, detail="Missing database")
    return land_lot


# SHOW REALTY WEBSOCKET
@app.websocket("/show-apartment")
async def show_realty_apartment_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            apartments = crud.get_realty_apartment(db)
            apartment_json = []
            for element in apartments:
                object_for_list = {
                    "id": element.id,
                    "city": element.city,
                    "area": element.area,
                    "street": element.street,
                    "price": element.price,
                    "floor": element.floor,
                    "rooms": element.rooms,
                }

                apartment_json.append(object_for_list)

            await websocket.send_text(json.dumps(apartment_json))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


@app.websocket("/show-temp-house")
async def show_realty_temp_house_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            temp_houses = crud.get_realty_temp_house(db)
            temp_house_json = []
            for element in temp_houses:
                object_for_list = {
                    "id": element.id,
                    "city": element.city,
                    "street": element.street,
                    "price": element.price,
                    "floor": element.floor,
                    "land_area": element.land_area,
                    "house_area": element.house_area,
                }

                temp_house_json.append(object_for_list)

            await websocket.send_text(json.dumps(temp_house_json))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


@app.websocket("/show-land-lot")
async def show_realty_land_lot_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            land_lots_db = crud.get_realty_land_lot(db)
            land_lots_json = []
            for element in land_lots_db:
                object_for_list = {
                    "id": element.id,
                    "city": element.city,
                    "street": element.street,
                    "price": element.price,
                    "area": element.area,
                }

                land_lots_json.append(object_for_list)

            await websocket.send_text(json.dumps(land_lots_json))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


# ADD REALTY WEBSOCKET
@app.websocket("/send-apartment")
async def send_apartments(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    token = websocket.query_params.get("token")
    print(token)

    if token is None:
        await websocket.close(code=400)
        return

    try:
        jwt_verification(token)
        data = await websocket.receive_json()  # apt for the table in json
        print(data)

        apart_dict = Dict2Class(data)
        crud.create_realty_apartment(db=db, realty=apart_dict, token=token)
        # apart = schema.Apartments(**data) !!

        await websocket.send_text("Data get apts")

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


@app.websocket("/send-temp-house")
async def send_temp_house(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    token = websocket.query_params.get("token")
    print(token)

    if token is None:
        await websocket.close(code=400)
        return

    try:
        jwt_verification(token)
        data = await websocket.receive_json()
        print(data)

        house_dict = Dict2Class(data)
        crud.create_realty_temp_house(db=db, realty=house_dict, token=token)

        await websocket.send_text("Data get apts")

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


@app.websocket("/send-land-lot")
async def send_land_lot(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    token = websocket.query_params.get("token")
    print(token)

    if token is None:
        await websocket.close(code=400)
        return

    try:
        jwt_verification(token)
        data = await websocket.receive_json()
        print(data)

        land_dict = Dict2Class(data)
        crud.create_realty_land_lot(db=db, realty=land_dict, token=token)

        await websocket.send_text("Data get apts")

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8400)
