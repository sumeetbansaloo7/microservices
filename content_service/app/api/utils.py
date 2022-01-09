from fastapi import HTTPException, status


def validate_content(content, id):
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Article with ID: {id} does not exist")
