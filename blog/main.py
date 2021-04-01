from fastapi import FastAPI
from . import schemas as sch

app = FastAPI()


@app.post('/blog')
def create(request : sch.Blog):
    return request