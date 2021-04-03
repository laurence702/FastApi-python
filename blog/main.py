from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas , models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound

app = FastAPI(
    title="FastApi Python",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["blog Endpoint"])
def create(request : schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', tags=["blog Endpoint"])
def get_posts(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, tags=["blog Endpoint"])
def show(id, response: Response, db:Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(post is None):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'blog with id of {id} not found', 'status' : False}
    else:
        return {'message': 'blog by id', 'data': post}

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=["blog Endpoint"])
def delete(id, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return f'post with id {id} deleted'

@app.put('/blog/{id}', tags=['Update'], status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request : schemas.Blog, db: Session=Depends(get_db)):
    #get blog by id
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with if {id} not found")
    else:
        blog.update({'title' : request.title, 'body' :  request.body})
        db.commit()
        return 'updated'