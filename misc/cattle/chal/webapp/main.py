import os

from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from classifier import Classifier
from validator import Validator

PHOTOS = [
    {"name": "Elephant", "url": "images/elephant.jpg", "label": "elephant"},
    {"name": "Dog", "url": "images/dog.jpg", "label": "golden_retriever"},
    {"name": "Cat", "url": "images/cat.jpg", "label": "tabby"},
    {"name": "Bird", "url": "images/bird.jpg", "label": "macaw"},
    {"name": "Tiger", "url": "images/tiger.jpg", "label": "tiger"},
    {"name": "Bee", "url": "images/bee.jpg", "label": "bee"},
]

FLAG = os.getenv("FLAG") or "TUDCTF{FAKE_FLAG}"

cls_instance = Classifier("static/imagenet_class_index.json")
validator_instance = Validator("static/images/hashes.json")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/allowed-photos")
async def read_allowed_photos(request: Request):
    return templates.TemplateResponse(
        request=request, name="allowed-photos.html", context={"photos": PHOTOS}
    )


@app.post("/upload")
async def upload_photo(request: Request, file: UploadFile):
    file_contents = await file.read()

    # Make sure that it's one of the allowed images.
    # Account for the fact that the image might have compression artifacts.
    if not validator_instance.validate(file_contents):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "Image not allowed!"},
        )

    # Get the predicted label
    predicted_label = cls_instance.classify(file_contents)

    if "spider" in predicted_label:  # What? Why? Why is there a spider?
        return templates.TemplateResponse(
            request=request, name="error.html", context={"error": str(globals())}
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="prediction.html",
            context={"prediction": predicted_label},
        )
