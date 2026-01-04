from typing import List, Optional
from app import db
from app.models import Document

class DocumentRepository:
    """Repository for Document database operations"""

    @staticmethod
    def create(document: Document) -> Document:
        db.session.add(document)
        db.session.commit()
        db.session.refresh(document)
        return document

    @staticmethod
    def get_by_id(document_id: int) -> Optional[Document]:
        """Get document by id"""
        return Document.query.get(document_id)

    @staticmethod
    def get_all(limit: int = 100, offset: int=0) -> List[Document]:
        """Get all documents"""
        return Document.query.order_by(Document.created_at.desc()).limit(limit).offset(offset).all()

    @staticmethod
    def update(document: Document) -> Document:
        """Update existing document"""
        db.session.commit()
        db.session.refresh(document)
        return document

    @staticmethod
    def delete(document: Document) -> None:
        """Delete document"""
        db.session.delete(document)
        db.session.commit()

    @staticmethod
    def search_by_title(query: str, limit: int = 10) -> List[Document]:
        """Search documents by title"""
        return Document.query.filter(
            Document.title.ilike(f"%{query}%")
        ).limit(limit).all()

    @staticmethod
    def get_by_tags(tags: List[str]) -> List[Document]:
        """Get all documents by tags"""
        # JSON contains query = check if tag is in the list
        return Document.query.filter(
            Document.tags.op('?|')(tags)
        ).all()
