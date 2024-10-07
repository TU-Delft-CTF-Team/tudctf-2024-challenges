import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.routes.room import router as room_router
from app.routes.user import router as user_router
from app.templates import TEMPLATES


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Load the rooms from the JSON file
    from app.rooms import load_rooms

    load_rooms("rooms.json")

    # Load the admin user from the environment variables
    admin_username = "admin"
    admin_email = "admin@example.com"
    full_name = "Annoying Administrator"
    password = os.getenv("ADMIN_PASSWORD", "admin")
    groups = ["staff"]

    # Register the admin user
    from app.users import register_user

    register_user(admin_username, admin_email, password, full_name, groups)

    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(user_router)
app.include_router(room_router)


@app.get("/")
async def read_root(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="index.html")


@app.get("/register")
async def read_register(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="register.html")


@app.get("/login")
async def read_login(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="login.html")


@app.get("/logout")
async def read_logout(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="logout.html")


@app.get("/users")
async def read_users(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="users.html")
