from typing import List, Optional, Dict
from app.models import Document
from app.repositories import DocumentRepository

class DocumentService:
    """Service layer for document business logic"""
    def __init__(self):
        self.repository = DocumentRepository()

    def create_document(self, title: str, content: str, source_type: str = 'manual',
                        source_url: Optional[str] = None) -> Document:
        """CREATE a new document with validation"""
        # Validation
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")

        if not content or len(content.strip()) == 0:
            raise ValueError("Content cannot be empty")

        if source_type not in ['manual', 'upload', 'web']:
            raise ValueError("Invalid source_type")

            # Create document
            document = Document(
                title=title.strip(),
                content=content.strip(),
                source_type=source_type,
                source_url=source_url
            )

            return self.repository.create(document)

    def get_document(self, document_id: int) -> Optional[Document]:
        """Get document by ID"""
        return self.repository.get_by_id(document_id)

    def list_documents(self, limit: int = 100, offset: int = 0) -> List[Document]:
        """List all documents with pagination"""
        return self.repository.get_all(limit=limit, offset=offset)

    def update_document(self, document_id: int, **kwargs) -> Optional[Document]:
        """Update document fields"""
        document = self.repository.get_by_id(document_id)

        if not document:
            return None

        # Update allowed fields

        allowed_fields = ['title', 'content', 'summary', 'source_url', 'tags']
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(document, field, value)

        return self.repository.update(document)

    def delete_document(self, document_id: int) -> bool:
        """Delete document"""
        document = self.repository.get_by_id(document_id)

        if not document:
            return False

        self.repository.delete(document)
        return True

