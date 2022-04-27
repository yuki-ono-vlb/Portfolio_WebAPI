from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from src.models.sns import Sns
from src.utils.database import get_session
from src.utils.authenticate import get_current_user
from urllib.parse import urlparse
import requests
import bs4

name = "sns"
router = APIRouter()
prefix = f"/{name}"
tags = [name]


@router.get("", response_model=List[Sns])
async def find_all(db: Session = Depends(get_session)):
    '''
    SNS情報を全て取得表示する
    '''
    return db.query(Sns).all()


@router.get("/{id}", response_model=Sns)
async def find(id: int, db: Session = Depends(get_session)):
    '''
    SNS情報をIDで絞り込んで取得
    '''
    sns = db.query(Sns).filter(Sns.id == id).first()
    if sns is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    return sns


@router.post("", response_model=Sns)
async def create(new_sns: Sns, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    SNS情報に新規登録をする
    '''
    if db.query(Sns).filter(Sns.sns_name == new_sns.sns_name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="該当と重複するデータが存在します。")
    
    parsed_uri = urlparse(new_sns.sns_url)
    new_sns.sns_favicon = f"https://www.google.com/s2/favicons?domain={parsed_uri.netloc}"
    try:
        db.add(new_sns)
        db.commit()
        db.refresh(new_sns)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの登録に失敗しました。")

    return new_sns


@router.put("", response_model=Sns)
async def modify(id: int, modify_sns: Sns, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    SNS情報を更新する
    '''
    sns: Sns = db.query(Sns).filter(Sns.id == modify_sns.id).first()
    if sns is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        sns.sns_name = modify_sns.sns_name
        sns.sns_url = modify_sns.sns_url
        db.commit()
        db.refresh(sns)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return sns


@router.delete("")
async def delete(id: int, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    SNS情報を削除する
    '''
    sns: Sns = db.query(Sns).filter(Sns.id == id).first()
    if sns is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        db.delete(sns)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return f"Complete Delete SKillname={sns.sns_name} "
