import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.models import Product, Products
from app.templates import TEMPLATES

# List of the products that the user can buy
PRODUCTS: list[Product] = []
# The secret flag that the user needs to get.
# It can be obtained by buying the flag item in the shop.
FLAG: str = "TUDCTF{FAKE_FLAG}"


# Structure that holds the user's data
@dataclass
class User:
    balance: int  # The user's balance
    products: list[Product]  # The products that the user has bought


# Variable that holds the user's data
USER_DATA = User(balance=1000, products=[])


# The function that sets up the application.
# It loads available products from the JSON file and sets the flag if it's on the server.
# It also sets up the user's data.
# It isn't something that the user can interact with.
@asynccontextmanager
async def lifespan(_: FastAPI):
    global PRODUCTS
    global FLAG

    # If we're on the server, load the secret flag.
    if "FLAG" in os.environ:
        FLAG = os.environ["FLAG"]

    # Load the products from the JSON file
    with open("products.json", "r") as file:
        products = Products.model_validate_json(file.read())
        PRODUCTS.extend(products.products)
    yield


# Create the application
app = FastAPI(lifespan=lifespan)
# Allow access to the static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Show a custom 404 page if the user tries to access a non-existent page
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return TEMPLATES.TemplateResponse(
            request=request, name="404.html", status_code=404
        )
    return await http_exception_handler(request, exc)


def get_response(request: Request, message: str | None = None):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "products": PRODUCTS,
            "user": USER_DATA,
            "flag": FLAG,
            "message": message,
        },
    )


@app.get("/")
async def get_index(request: Request):
    # Just show the page.
    return get_response(request)


# Post request indicates that the user wants to buy a product
@app.post("/")
async def post_index(
    request: Request,
    product_id: Annotated[int, Form()],  # Get the product id from the form
    product_price: Annotated[int, Form()],  # Get the product price from the form
):
    global USER_DATA

    # Find the product with the given id
    product = next(filter(lambda x: x.id == product_id, PRODUCTS))

    # Check if the user has enough balance to buy the product
    if product.price > USER_DATA.balance:
        # Show a message that the user is too broke to buy the product
        return get_response(request, "You are too broke to buy this product")

    # Deduct the product price from the user's balance and add the product to the user's products
    USER_DATA.balance -= product_price
    USER_DATA.products.append(product)

    # Show a message that the user bought the product
    return get_response(request, f"You bought {product.name} for {product.price}!")
