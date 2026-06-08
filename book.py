from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
    title : str
    rating: int
    director : str

@app.post("/movie")
def create_movie(movie: Movie):
    return {
        "Title" : movie.title,
        "Rating": movie.rating
    }