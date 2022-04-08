from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from src.models.history import History
from src.utils.database import get_session
from src.utils.authenticate import get_current_user
name = "history"
router = APIRouter()
prefix = f"/{name}"
tags = [name]


@router.get("", response_model=History)
async def find_all(db: Session = Depends(get_session)):
    '''
    経歴情報を全て取得表示する
    '''
    return db.query(History).all()


@router.get("/{id}", response_model=History)
async def find(id: int, db: Session = Depends(get_session)):
    '''
    経歴情報をIDで絞り込んで取得
    '''
    history = db.query(History).filter(History.id == id).first()
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    return history


@router.post("", response_model=History)
async def create(new_history: History, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    経歴情報に新規登録をする
    '''
    if db.query(History).filter(History.name == new_history.name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="該当と重複するデータが存在します。")

    try:
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの登録に失敗しました。")

    return new_history


@router.put("", response_model=History)
async def modify(id: int, modify_history: History, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    経歴情報を更新する
    '''
    history: History = db.query(History).filter(
        History.id == modify_history.id).first()
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        history.description = modify_history.description
        history.histroy_day = modify_history.histroy_day

        db.commit()
        db.refresh(history)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return history


@router.delete("")
async def delete(id: int, db: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    '''
    経歴情報を削除する
    '''
    history: History = db.query(History).filter(History.id == id).first()
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="該当のデータは存在しませんでした。")

    try:
        db.delete(history)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="データベースの更新に失敗しました。")

    return f"Complete Delete SKillname={history.history_name} "
