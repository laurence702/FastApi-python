from fastapi import APIRouter
from .. import schemas, database, models
from typing import List

router = APIRouter()

@router.get('/blog', response_model= List[schemas.ShowBlog], tags=["blog Endpoint"])
def get_posts(db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
