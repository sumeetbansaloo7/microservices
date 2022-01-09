from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import dbmodels
from .schemas import *
from .database import get_db
from sqlalchemy.exc import IntegrityError
from .utils import validate_credentials
user = APIRouter(
    prefix="/user",
    tags=['User']
)


@user.post('/', status_code=201, response_model=UserBase)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    new_user = dbmodels.User(**payload.dict())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with Email: {payload.email} already exists")
    db.refresh(new_user)
    return new_user


@user.get('/{email}', response_model=UserBase)
def get_user(email: EmailStr, db: Session = Depends(get_db)):

    user = db.query(dbmodels.User).filter(dbmodels.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with Email: {email} does not exist")
    return user


@user.post('/validate', response_model=UserBase)
def validate_user(payload: UserValidte, db: Session = Depends(get_db)):
    user = db.query(dbmodels.User).filter(
        dbmodels.User.email == payload.email).first()
    validate_credentials(user=user, payload=payload)
    return user


@user.put('/', response_model=UserBase)
def update_user(payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(dbmodels.User).filter(dbmodels.User.email ==
                                          payload.email)
    user_query = user.first()
    validate_credentials(user_query, payload=payload)
    payload = payload.dict()
    password = payload.pop('password')
    email = payload.pop('email')
    new_email = payload.pop('new_email')
    new_password = payload.pop('new_password')
    if new_email:
        try:
            user.update({"email": new_email}, synchronize_session=False)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with Email: {new_email} already exists")
    if new_password:
        user.update({"password": new_password}, synchronize_session=False)
    for key in payload:
        if payload[key]:
            user.update({key: payload[key]}, synchronize_session=False)
    db.commit()
    db.refresh(user_query)

    return user_query


@user.delete('/')
def delete_user(payload: UserDelete, db: Session = Depends(get_db)):

    user = db.query(dbmodels.User).filter(dbmodels.User.email ==
                                          payload.email)

    user_query = user.first()
    validate_credentials(user=user_query, payload=payload)
    user.delete(synchronize_session=False)
    db.commit()
    return {'message': 'User deleted successfully!!'}
