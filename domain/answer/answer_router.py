from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_crud, answer_schema
from domain.answer.answer_crud import get_answer
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix='/api/answer'
)


@router.post('/create/{answer_id}', status_code=status.HTTP_204_NO_CONTENT)
def answer_create(answer_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    answer = get_answer(db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail='answer not found!')
    answer_crud.create_answer(db,
                              answer_create=_answer_create,
                              answer=answer,
                              user=current_user)

    # redirect
    # from domain.answer.answer_router import router as answer_router
    # url = answer_router.url_path_for('/answer/detail',
    #                                    answer_id=answer_id)
    # return RedirectResponse(url, status_code=303)


@router.get('/detail/{answer_id}', response_model=answer_schema.Answer)
def answer_get(answer_id: int, db: Session = Depends(get_db)):
    return answer_crud.get_answer(db=db,
                                  answer_id=answer_id)


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="수정권한이 없습니다.")
    answer_crud.update_answer(db=db,
                              db_answer=db_answer,
                              answer_update=_answer_update)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)


@router.post('/vote', status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db=db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    answer_crud.vote_answer(db=db, db_answer=db_answer, db_user=user)
