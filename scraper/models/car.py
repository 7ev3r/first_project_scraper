from typing import Optional
from pydantic import BaseModel


class Car(BaseModel):
    cars: str
    prices: str
    descriptions: str
    car_links: str

class CarLink(BaseModel):
    url: str