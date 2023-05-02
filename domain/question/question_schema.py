from __future__ import annotations

import datetime
import typing

from pydantic import BaseModel, validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: typing.Union[User, None]
    modify_date: typing.Union[datetime.datetime, None] = None
    voter: list[User] = []

    class Config:
        orm_mode = True


class QuestionList(BaseModel):
    total: int
    question_list: list[Question] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int