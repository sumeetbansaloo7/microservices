from fastapi import FastAPI, Depends
# from fastapi.params import Depends
from sqlalchemy.orm import Session
from .api.routes import event
from .api.database import engine, get_db
from .api import dbmodels
from .api.dbmodels import EventRead, EventLike

dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def index(db: Session = Depends(get_db)):
    return {"Event Service": "Running 😊"}
app.include_router(event)
