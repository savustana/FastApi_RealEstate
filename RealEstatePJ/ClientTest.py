from websockets import connect
import asyncio
from main import SECRET_KEY
from datetime import datetime
import jwt
import json
import time


def create_jwt_token():
    pay = {
        "sub": "user_id",
        "exp": time.time() + 200
    }
    return jwt.encode(pay, "SECRET_KEY", algorithm="HS256")


object_temp_house = {
                    "city": "Kyiv",
                    "house_area": 200,
                    "street": "Lesia Ukrainky",
                    "price": 457000,
                    "floor": 2,
                    "land_area": 600,
                }

object_apartment = {
                    "city": "Kyiv",
                    "area": 100,
                    "street": "Lesia Ukrainky",
                    "price": 500000,
                    "floor": 12,
                    "rooms": 4,
                }

object_land_lot = {
                    "city": "Kyiv",
                    "area": 100,
                    "street": "Lesia Ukrainky",
                    "price": 500000,
                }


async def send_apartment():
    token = create_jwt_token()
    web_uri = f'ws://localhost:8400/send-apartment?token={token}'
    async with connect(web_uri) as web:
        await web.send(json.dumps(object_apartment))
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


async def test_get_apartment():
    web_uri = 'ws://localhost:8400/show-apartment'
    async with connect(web_uri) as web:
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


async def test_get_temp_house():
    web_uri = 'ws://localhost:8400/show-temp-house'
    async with connect(web_uri) as web:
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


async def test_get_land_lot():
    web_uri = 'ws://localhost:8400/show-land-lot'
    async with connect(web_uri) as web:
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


async def send_temp_house():
    token = create_jwt_token()
    web_uri = f'ws://localhost:8400/send-temp-house?token={token}'
    async with connect(web_uri) as web:
        await web.send(json.dumps(object_temp_house))
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


async def send_land_lot():
    token = create_jwt_token()
    print(token)
    web_uri = f'ws://localhost:8400/send-land-lot?token={token}'
    async with connect(web_uri) as web:
        await web.send(json.dumps(object_land_lot))
        data = await web.recv()
        print(data)
        await asyncio.sleep(1)


# asyncio.run(test_get_apartment())
# asyncio.run(test_get_temp_house())
# asyncio.run(test_get_land_lot())

asyncio.run(send_apartment())
asyncio.run(send_temp_house())
asyncio.run(send_land_lot())
