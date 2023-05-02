from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_crud
from domain.question import question_schema
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix='/api/question'
)


@router.get('/list', response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, page * size, size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }


@router.get('/detail/{question_id}', response_model=question_schema.Question)
def question(question_id: int, db: Session = Depends(get_db)):
    _question = question_crud.get_question(db, question_id)
    return _question


@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def create_question(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db,
                                  question_create=_question_create,
                                  user=current_user)


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def update_question(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="수정권한이 없습니다.")
    question_crud.update_question(db=db,
                                  db_question=db_question,
                                  question_update=_question_update)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_question(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="삭제권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)


@router.post('/vote', status_code=status.HTTP_204_NO_CONTENT)
def vote_question(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db=db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    question_crud.vote_question(db=db, db_question=db_question, db_user=user)
