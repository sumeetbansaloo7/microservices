from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .api.routes import content
from .api.database import engine, get_db
from .api import dbmodels
from .api.dbmodels import Content

dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def index(db: Session = Depends(get_db)):
    return {"Content Service": "Running 😊"}
app.include_router(content)
