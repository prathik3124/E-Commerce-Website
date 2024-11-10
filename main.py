from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path


# Local Imports.
from backend.src.trending import get_top_ten_trending
from backend.src.item_rec_sys import get_similar_items
from backend.src.user_rec_sys import get_top_n_recommendations

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent.absolute() / "frontend/static"), name="static")


@app.get("/")
def homepage(request: Request):
    """
    Displays Homepage and Top Trending.

    """
    top_ten_trending = get_top_ten_trending()
    return templates.TemplateResponse("homepage.html", {
        "request": request,
        "top_ten_trending": top_ten_trending
    })


@app.get("/about")
def about(request: Request):
    """
    Displays About page.
    """
    return templates.TemplateResponse("about.html", {
        "request": request
    })


class ItemRec(BaseModel):
    """
    Validating POST request by user in the 'Find Similar Products' section.
    """
    item_raw_id: str


@app.post("/item_rec")
def item_rec(item_rec: ItemRec):
    """
    Generates similar products using input in the 'Find Similar Products' section.

    """
    user_input_raw_id = item_rec.item_raw_id
    similar_items = get_similar_items(user_input_raw_id)
    return {
        "similar_items": similar_items
    }


class UserRec(BaseModel):
    """
    Validating POST request by user in the 'Products you might like' section.

    """
    item_raw_id: str
    review_score: int


@app.post("/user_rec")
def user_rec(user_rec: UserRec):
    """
    Generates product recommendations using input in the 'Products you might like' section.

    """
    user_input_raw_id = user_rec.item_raw_id
    user_input_review_score = user_rec.review_score
    top_recommends = get_top_n_recommendations(user_input_raw_id,
                                               user_input_review_score,
                                               n_recommendations=3)
    return {
        "top_recommends": top_recommends
    }
