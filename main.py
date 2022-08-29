from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from data_get import all_result, config_result
from data_post import config_set

app = FastAPI()

# instalacja fastapi razem z uvicorn
# pip install fastapi[all]

# instalacja driver do MariaDB
# pip install mariadb

# start serwera --reolad pcja pod developmnet, restartuje serwer po zminach kodu
# uvicorn main:app --reload


class Config(BaseModel):
    temp_w: float
    temp_e: float
    dimension_x: int
    dimension_y: int
    dimension_z: int

# dane do wykresu temperatury
@app.get("/mariadb/chart")
async def read_item_chart():
    return all_result()

# pobranie aktualnej konfiguracji
@app.get("/mariadb/config")
async def read_item_config():
    return config_result()

# ustawienie nowej konfiguracji
@app.post("/mariadb/set/")
async def set_config(json: Config):
    return config_set(json)




