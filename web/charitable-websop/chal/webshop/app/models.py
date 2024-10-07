from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: int
    description: str
    image: str


class Products(BaseModel):
    products: list[Product]
