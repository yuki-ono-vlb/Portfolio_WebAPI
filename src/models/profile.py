from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Profile(SQLModel, table=True):
    '''
    プロフィール情報
    '''
    
    '''
    プロフィール情報ID
    '''
    id: Optional[int] = Field(default=None,primary_key=True,index=True)
    
    '''
    氏名
    '''
    name: str

    '''
    氏名(ひらがな)
    '''
    name_hiragana: str
    
    '''
    性別
    '''
    sex: int
    
    '''
    生年月日
    '''
    birthday:date
    
    '''
    血液型
    '''
    blood_type: int
