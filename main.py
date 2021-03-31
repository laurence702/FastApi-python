from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data' : {
        'name' : 'Toyosi Moi-Moi'
    }}

@app.get('/about')
def about():
    return {'data':'about page'}