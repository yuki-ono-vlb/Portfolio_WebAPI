from typing import Optional
from sqlmodel import Field, SQLModel

class Sns(SQLModel, table=True):
    '''
    SNS情報
    '''
    
    '''
    SNS情報ID
    '''
    id: Optional[int] = Field(default=None,primary_key=True,index=True)
    
    '''
    SNS名
    '''
    sns_name: str
    
    '''
    SNS URL
    '''
    sns_url:str