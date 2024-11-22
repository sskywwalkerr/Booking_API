from pydantic import BaseModel
from typing import List


class item_basePrice(BaseModel):
    item_basePrice: str


class products(BaseModel):
    products: List[item_basePrice]
