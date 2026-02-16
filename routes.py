from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text

from db import get_db

router = APIRouter()

# ----------- Request models (schemas) -----------

class RegisterIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    birth_date: Optional[str] = None  # "YYYY-MM-DD"
    gender: Optional[str] = None      # 1 char like "M"
    bio: Optional[str] = None
    status: str = "active"            # must match your enum user_status

class PostQuestionIn(BaseModel):
    author_id: int
    title: str
    body: str
    status: str = "open"              # must match your enum question_status

class PostAnswerIn(BaseModel):
    question_id: int
    author_id: int
    body: str

class VoteIn(BaseModel):
    voter_id: int
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    vote: int  # usually 1 or -1

class CommentIn(BaseModel):
    author_id: int
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    body: str

# ----------- Helper -----------

def exactly_one_is_set(a, b) -> bool:
    # True if exactly one is not None
    return (a is None) ^ (b is None)

# ----------- Endpoints -----------

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    rows = db.execute(
        text("""
            SELECT user_id, first_name, last_name, email, username, joined_at, status
            FROM users
            ORDER BY user_id DESC
            LIMIT 50
        """)
    ).mappings().all()
    return {"items": list(rows)}

@router.post("/users/register")
def register_user(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        row = db.execute(
            text("""
                SELECT register(
                    :first_name, :last_name, :email, :username, :password,
                    :phone_number, :address, :city, :country,
                    CAST(:birth_date AS date),
                    CAST(:gender AS char(1)),
                    :bio,
                    CAST(:status AS user_status)
                ) AS ok
            """),
            payload.dict()
        ).mappings().first()

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    if not row or not row["ok"]:
        raise HTTPException(status_code=400, detail="Registration failed")

    return {"success": True}

@router.post("/questions")
def create_question(payload: PostQuestionIn, db: Session = Depends(get_db)):
    try:
        row = db.execute(
            text("""
                SELECT post_question(
                    :author_id, :title, :body, :status::question_status
                ) AS ok
            """),
            payload.dict()
        ).mappings().first()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": bool(row and row["ok"])}

@router.get("/questions")
def list_questions(db: Session = Depends(get_db)):
    rows = db.execute(
        text("""
            SELECT question_id, author_id, title, status, created_at, updated_at
            FROM questions
            ORDER BY question_id DESC
            LIMIT 50
        """)
    ).mappings().all()
    return {"items": list(rows)}

@router.post("/answers")
def create_answer(payload: PostAnswerIn, db: Session = Depends(get_db)):
    try:
        row = db.execute(
            text("SELECT post_answer(:question_id, :author_id, :body) AS ok"),
            payload.dict()
        ).mappings().first()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": bool(row and row["ok"])}

@router.post("/votes")
def vote(payload: VoteIn, db: Session = Depends(get_db)):
    if not exactly_one_is_set(payload.question_id, payload.answer_id):
        raise HTTPException(status_code=400, detail="Provide exactly one of question_id or answer_id")

    try:
        row = db.execute(
            text("SELECT make_vote(:voter_id, :question_id, :answer_id, :vote) AS ok"),
            payload.dict()
        ).mappings().first()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": bool(row and row["ok"])}

@router.post("/comments")
def comment(payload: CommentIn, db: Session = Depends(get_db)):
    if not exactly_one_is_set(payload.question_id, payload.answer_id):
        raise HTTPException(status_code=400, detail="Provide exactly one of question_id or answer_id")

    try:
        row = db.execute(
            text("SELECT make_comment(:author_id, :question_id, :answer_id, :body) AS ok"),
            payload.dict()
        ).mappings().first()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": bool(row and row["ok"])}