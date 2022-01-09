import os
from fastapi import HTTPException
import httpx

CONTENT_SERVICE_HOST_URL = os.environ.get(
    'CONTENT_SERVICE_HOST_URL')  # 'http://localhost:8002/content'
USER_SERVICE_HOST_URL = os.environ.get(
    'USER_SERVICE_HOST_URL')  # 'http://localhost:8001/user'


def is_content_service_up():
    r = httpx.get(CONTENT_SERVICE_HOST_URL)
    return True if r.status_code == 200 else False


def is_user_service_up():
    r = httpx.get(USER_SERVICE_HOST_URL)
    return True if r.status_code == 200 else False


def validate_user(email, password):
    r = httpx.post(f'{USER_SERVICE_HOST_URL}/validate',
                   json={"email": email, "password": password})
    return dict(r.json()) if r.status_code == 200 else int(r.status_code)


def validate_content(contentid):
    r = httpx.get(f'{CONTENT_SERVICE_HOST_URL}/{contentid}')
    # print(r.url)
    return r.status_code


def update_content(payload):
    try:
        r = httpx.put(f'{CONTENT_SERVICE_HOST_URL}/', json=payload)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail=f"User Service is down 😓")

    return True if r.status_code == 200 else False
