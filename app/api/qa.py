from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db.base import get_db
from app.db.models import User, QAHistory
from app.services.qa_service import QAService
from app.api.auth import get_current_user

router = APIRouter()

class Question(BaseModel):
    text: str
    document_id: Optional[int] = None

class QAHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
    document_id: int

    class Config:
        from_attributes = True

@router.post("/ask")
def ask_question(
    question: Question,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    qa_service = QAService(db)
    answer = qa_service.ask_question(
        question=question.text,
        user_id=current_user.id,
        document_id=question.document_id
    )
    return {"answer": answer}

@router.get("/history", response_model=List[QAHistoryResponse])
def get_qa_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    qa_service = QAService(db)
    return qa_service.get_qa_history(current_user.id) 