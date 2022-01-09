from fastapi import HTTPException, status


def validate_credentials(user, payload):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with Email: {payload.email} does not exist")
    else:
        if user.password != payload.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Incorrect Password. Try again")
