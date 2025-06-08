from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.db.base import get_db
from app.db.models import User
from app.services.document_service import DocumentService
from app.api.auth import get_current_user

router = APIRouter()

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    is_selected: bool
    created_at: str

    class Config:
        from_attributes = True

class DocumentSelection(BaseModel):
    is_selected: bool

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_service = DocumentService(db)
    return document_service.create_document(
        title=document.title,
        content=document.content,
        user_id=current_user.id
    )

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_service = DocumentService(db)
    return document_service.get_user_documents(current_user.id)

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_service = DocumentService(db)
    if document_service.delete_document(document_id, current_user.id):
        return {"message": "Document deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )

@router.put("/{document_id}/select", response_model=DocumentResponse)
def update_document_selection(
    document_id: int,
    selection: DocumentSelection,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_service = DocumentService(db)
    document = document_service.update_document_selection(
        document_id,
        current_user.id,
        selection.is_selected
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document 