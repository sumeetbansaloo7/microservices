from fastapi import HTTPException, status
from .service import is_content_service_up, is_user_service_up, validate_content, validate_user


def validate_services():
    if is_content_service_up():
        print("Content Service Running")
    if is_user_service_up():
        print("User Service Running")


def validate_user_and_content(payload):
    res = {'valid': False}
    response = ""
    try:
        response = validate_user(payload.email, payload.password)
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"User Service is down 😓")
    if type(response) is int:
        user_validation_failed(response, payload)
    if type(response) is dict:
        res["userid"] = response['id']

    try:
        response = validate_content(payload.contentid)
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Content Service is down 😓")
    if response == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Article with ID: {payload.contentid} does not exist")
    res["valid"] = True
    return res


def user_validation_failed(response, payload):
    if response == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with Email: {payload.email} does not exist")
    elif response == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect Password. Try again")
