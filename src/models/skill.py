from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Skill(SQLModel, table=True):
    '''
    スキル情報
    '''
    
    '''
    スキル情報ID
    '''
    id: Optional[int] = Field(default=None,primary_key=True,index=True)
    
    '''
    スキル名
    '''
    skill_name: str
    
    '''
    業務開始年月
    '''
    working_day:date
    
    '''
    学習開始年月
    '''
    study_day:date
    
    '''
    フレームワーク
    '''
    framework:str