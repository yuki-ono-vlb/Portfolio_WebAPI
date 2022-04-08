from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from src.models.profile import Profile
from src.utils.database import get_session
from src.utils.authenticate import get_current_user

name = "profile"
router = APIRouter()
prefix = f"/{name}"
tags = [name]


@router.get("", response_model=List[Profile])
async def find_all(db: Session = Depends(get_session)):
    '''
    プロフィール情報を全て取得表示する
    '''
    return db.query(Profile).all()


@router.get("/{id}", response_model=Profile)
async def find(id: int, db: Session = Depends(get_session)):
    '''
    プロフィール情報をIDで絞り込んで取得
    '''
    profile = db.query(Profile).filter(Profile.id == id).first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    return profile


@router.post("", response_model=Profile)
async def create(new_profile: Profile, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    プロフィール情報に新規登録をする
    '''
    if db.query(Profile).filter(Profile.name == new_profile.name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="該当と重複するデータが存在します。")

    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの登録に失敗しました。")

    return new_profile


@router.put("", response_model=Profile)
async def modify(id: int, modify_profile: Profile, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    プロフィール情報を更新する
    '''
    profile: Profile = db.query(Profile).filter(
        Profile.id == modify_profile.id).first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        profile.name = modify_profile.name
        profile.name_hiragana = modify_profile.name_hiragana
        profile.sex = modify_profile.sex
        profile.birthday = modify_profile.birthday
        profile.blood_type = modify_profile.blood_type

        db.commit()
        db.refresh(profile)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return profile


@router.delete("")
async def delete(id: int, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    プロフィール情報を削除する
    '''
    profile: Profile = db.query(Profile).filter(Profile.id == id).first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        db.delete(profile)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return f"Complete Delete SKillname={profile.profile_name} "
