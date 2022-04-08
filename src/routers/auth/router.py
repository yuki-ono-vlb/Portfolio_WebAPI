from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.utils.database import get_session
from src.models.user import User
from src.utils.hash import Hash
from src.utils.authenticate import create_access_token
from src.utils import auth

router = APIRouter()
prefix = "/auth"
tags = ['authentication']


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(User).filter(
        User.user_name == request.username).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )
    if not Hash.verify_password(user.hashed_password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
        )
    access_token = create_access_token(data={'sub': user.user_name})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.user_name
    }


