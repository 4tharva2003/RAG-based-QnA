from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Document
from app.services.embedding_service import embedding_service

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(self, title: str, content: str, user_id: int) -> Document:
        """Create a new document with its embedding."""
        embedding = embedding_service.generate_embedding(content)
        document = Document(
            title=title,
            content=content,
            embedding=embedding,
            user_id=user_id
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def get_document(self, document_id: int, user_id: int) -> Optional[Document]:
        """Get a document by ID for a specific user."""
        return self.db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
    
    def get_user_documents(self, user_id: int) -> List[Document]:
        """Get all documents for a specific user."""
        return self.db.query(Document).filter(Document.user_id == user_id).all()
    
    def delete_document(self, document_id: int, user_id: int) -> bool:
        """Delete a document by ID for a specific user."""
        document = self.get_document(document_id, user_id)
        if document:
            self.db.delete(document)
            self.db.commit()
            return True
        return False
    
    def update_document_selection(self, document_id: int, user_id: int, is_selected: bool) -> Optional[Document]:
        """Update the selection status of a document."""
        document = self.get_document(document_id, user_id)
        if document:
            document.is_selected = is_selected
            self.db.commit()
            self.db.refresh(document)
        return document
    
    def get_selected_documents(self, user_id: int) -> List[Document]:
        """Get all selected documents for a specific user."""
        return self.db.query(Document).filter(
            Document.user_id == user_id,
            Document.is_selected == True
        ).all() 