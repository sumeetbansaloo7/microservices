from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import dbmodels
from .schemas import *
from .database import get_db
from .utils import validate_services, validate_user_and_content
from .service import update_content, USER_SERVICE_HOST_URL
import httpx
event = APIRouter(
    prefix="/event",
    tags=['Event']
)


@event.get('/services', status_code=200)
def validate_other_services():
    print("canged")
    try:
        validate_services()
        r = httpx.get(f'{USER_SERVICE_HOST_URL}')
        print(r.url)
        print(r.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Services are down 😓")
    return {"message": "All Services Running 😊"}


@event.post('/like', status_code=200, response_model=EventBaseLiked)
def like_content(payload: EvenLike, db: Session = Depends(get_db)):
    userid = None
    event = None
    res = validate_user_and_content(payload)
    if not res['valid']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid details provided.")

    res['contentid'] = payload.contentid
    res.pop('valid')
    event = db.query(dbmodels.EventLike).filter(
        dbmodels.EventLike.userid == res["userid"], dbmodels.EventLike.contentid == res["contentid"]).first()

    if not event:
        res['likedflag'] = True
        new_event = dbmodels.EventLike(**res)
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        update_content({
            "id": res['contentid'],
            "likeordislike": "like"
        })
        return new_event
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Already Liked")


@event.post('/markread', status_code=200, response_model=EventBaseRead)
def mark_read_content(payload: EvenRead, db: Session = Depends(get_db)):
    userid = None
    event = None
    res = validate_user_and_content(payload)
    if not res['valid']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid details provided.")

    res['contentid'] = payload.contentid
    res.pop('valid')
    event = db.query(dbmodels.EventRead).filter(
        dbmodels.EventRead.userid == res["userid"], dbmodels.EventRead.contentid == res["contentid"]).first()

    if not event:
        res['readflag'] = True
        new_event = dbmodels.EventRead(**res)
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        update_content({
            "id": res['contentid'],
            "readorunread": "read"
        })
        return new_event
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Already Read")
