from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel


class History(SQLModel, table=True):
    '''
    経歴情報
    '''

    '''
    プロフィール情報ID
    '''
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    '''
    説明
    '''
    description: str
    
    '''
    経歴年月
    '''

    '''
    学習開始年月
    '''
    histroy_day: date
