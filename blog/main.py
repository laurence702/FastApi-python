from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from . import schemas , models
from .hashing import HashPassword
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title="FastApi Python",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)

models.Base.metadata.create_all(engine)

get_db = database.get_db


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["blog Endpoint"])
def create(request : schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog) 
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.post('/user',response_model= schemas.ShowUser,tags=['User Endpoint'], status_code=status.HTTP_202_ACCEPTED)
def create_user(request : schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=HashPassword.hash_this(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
@app.get('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog, tags=["blog Endpoint"])
def show(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")
    return blog

@app.get('/user/{id}', status_code=status.HTTP_202_ACCEPTED, response_model= schemas.ShowUser,tags=['User Endpoint'])
def get_users(id : int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")
    return user

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=["blog Endpoint"])
def delete(id, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        return "Deleted"
    
@app.put('/blog/{id}', tags=['blog Endpoint'], status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request : schemas.Blog, db: Session=Depends(get_db)):
    #get blog by id
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with if {id} not found")
    else:
        blog.update({'title' : request.title, 'body' :  request.body})
        db.commit()
        return 'updated'