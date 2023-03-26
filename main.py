from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import randomizer as app_random

app = FastAPI()
app.mount("/static", StaticFiles(directory="./web/static"), name="static")
templates = Jinja2Templates(directory="./web/templates")
img_path = Path('./web/static/img').resolve()


@app.get('/')
def root(request: Request):
    images: List[Path] = app_random.get_images(img_path)

    if len(images) < 1:
        return 'No images found!'

    rand_number: int = app_random.get_rand_number(1, len(images) - 1)
    selection: Path = images[rand_number]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "selection_filename": selection.name,
            "selection_title": selection.stem,
        },
    )
