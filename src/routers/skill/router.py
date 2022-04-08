from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from src.models.skill import Skill
from src.utils.database import get_session
from src.utils.authenticate import get_current_user


name = "skill"
router = APIRouter()
prefix = f"/{name}"
tags = [name]


@router.get("", response_model=List[Skill])
async def find_all(db: Session = Depends(get_session)):
    '''
    スキル情報を全て取得表示する
    '''
    return db.query(Skill).all()


@router.get("/{id}", response_model=Skill)
async def find(id: int, db: Session = Depends(get_session)):
    '''
    スキル情報をIDで絞り込んで取得
    '''
    skill = db.query(Skill).filter(Skill.id == id).first()
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    return skill


@router.post("", response_model=Skill)
async def create(new_skill: Skill, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    スキル情報に新規登録をする
    '''
    if db.query(Skill).filter(Skill.skill_name == new_skill.skill_name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="該当と重複するデータが存在します。")

    try:
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの登録に失敗しました。")

    return new_skill


@router.put("", response_model=Skill)
async def modify(modify_skill: Skill, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    スキル情報を更新する
    '''
    skill: Skill = db.query(Skill).filter(Skill.id == modify_skill.id).first()
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        skill.skill_name = modify_skill.skill_name
        skill.working_day = modify_skill.working_day
        skill.study_day = modify_skill.study_day
        skill.framework = modify_skill.framework
        db.commit()
        db.refresh(skill)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return skill


@router.delete("")
async def delete(id: int, db: Session = Depends(get_session), current_user:str = Depends(get_current_user)):
    '''
    スキル情報を削除する
    '''

    skill: Skill = db.query(Skill).filter(Skill.id == id).first()
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        db.delete(skill)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return f"Complete Delete SKillname={skill.skill_name} "
