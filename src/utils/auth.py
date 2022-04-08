from fastapi import HTTPException, status
from sqlmodel import Session
from src.models.user import User
from src.utils.hash import Hash

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.user_name == username).first()
    if not username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {username} not found')
    return user


def create_user(db: Session, request: User):
    new_user = User(
        user_name=request.user_name,
        email=request.email,
        hashed_password=Hash.get_password_hash(request.hashed_password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
