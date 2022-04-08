from datetime import date
import email
from typing import Optional
from sqlmodel import Field, SQLModel


class ModelUser(SQLModel):
    '''
    ユーザー名
    '''
    user_name: str

    '''
    email
    '''
    email: str
    

class User(ModelUser, table=True):
    '''
    ユーザー情報
    '''
    
    '''
    ユーザー情報ID
    '''
    id: Optional[int] = Field(default=None,primary_key=True,index=True)
    
    
    '''
    パスワード
    '''
    hashed_password: str
    
    is_active:bool = Field(default=True)

