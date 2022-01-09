from fastapi import APIRouter, Depends, File, UploadFile
from typing import List
from sqlalchemy.orm import Session
from . import dbmodels
from .schemas import *
from .database import get_db, engine
from .utils import validate_content
import pandas as pd
from io import StringIO

content = APIRouter(
    prefix="/content",
    tags=['Content']
)


@content.post('/bulk', status_code=201)
def create_content_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(
        StringIO(str(file.file.read(), 'utf-8')), encoding='utf-8')

    df.to_sql('content', con=engine, if_exists='append', index=False)
    print(df.head(10))
    return {"message": "data added successfully"}


@content.post('/', status_code=201, response_model=ContentBase)
def create_content(payload: ContentCreate, db: Session = Depends(get_db)):
    new_content = dbmodels.Content(**payload.dict())
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


@content.get('/all', response_model=List[ContentBase])
def get_content_all(db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).all()
    validate_content(content, id)
    return content


@content.get('/mostliked/{count}', response_model=List[ContentBase])
def get_content_mostliked(count: int, db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).order_by(
        dbmodels.Content.total_likes.desc())[0:count]
    return content


@content.get('/mostread/{count}', response_model=List[ContentBase])
def get_content_mostliked(count: int, db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).order_by(
        dbmodels.Content.total_reads.desc())[0:count]
    return content


@content.get('/latest/{count}', response_model=List[ContentBase])
def get_content_latest(count: int, db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).order_by(
        dbmodels.Content.date_published.desc())[0:count]
    return content


@content.get('/topinteracted/{count}', response_model=List[ContentBase])
def get_content_topinteracted(count: int, db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).order_by(
        dbmodels.Content.total_reads.desc()).order_by(
        dbmodels.Content.total_likes.desc())[0:count]
    return content


@content.get('/{id}', response_model=ContentBase)
def get_content(id: int, db: Session = Depends(get_db)):

    content = db.query(dbmodels.Content).filter(
        dbmodels.Content.id == id).first()
    validate_content(content, id)
    return content


@content.put('/', response_model=ContentBase)
def update_content(payload: ContentUpdate, db: Session = Depends(get_db)):
    content = db.query(dbmodels.Content).filter(dbmodels.Content.id ==
                                                payload.id)
    content_query = content.first()
    validate_content(content_query, payload.id)
    payload = payload.dict()
    id = payload.pop('id')
    if payload['likeordislike']:
        if payload['likeordislike'].lower().strip() == 'like':
            content.update(
                {'total_likes': content_query.total_likes+1}, synchronize_session=False)
        elif payload['likeordislike'].lower().strip() == 'dislike':
            content.update(
                {'total_likes': content_query.total_likes-1 if content_query.total_likes > 1 else 0}, synchronize_session=False)
    payload.pop('likeordislike')
    if payload['readorunread']:
        if payload['readorunread'].lower().strip() == 'read':
            content.update(
                {'total_reads': content_query.total_reads+1}, synchronize_session=False)
        elif payload['readorunread'].lower().strip() == 'unread':
            content.update(
                {'total_reads': content_query.total_reads-1 if content_query.total_reads > 1 else 0}, synchronize_session=False)
    payload.pop('readorunread')
    for key in payload:
        if payload[key]:
            content.update({key: payload[key]}, synchronize_session=False)
    db.commit()
    db.refresh(content_query)
    return content_query


@content.delete('/{id}')
def delete_content(id: int, db: Session = Depends(get_db)):

    content = db.query(dbmodels.Content).filter(dbmodels.Content.id == id)
    content_query = content.first()
    validate_content(content_query, id)
    content.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Article deleted successfully!!'}
