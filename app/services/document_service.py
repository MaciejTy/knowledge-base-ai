from typing import List, Optional, Dict
from app.models import Document
from app.repositories import DocumentRepository
from app.services.ai_service import AIService


class DocumentService:
    """Service layer for document business logic"""

    def __init__(self):
        self.repository = DocumentRepository()
        self.ai_service = AIService()

    def create_document(self, title: str, content: str, source_type: str = 'manual',
                        source_url: Optional[str] = None, use_ai: bool = True) -> Document:
        """
        Create a new document with validation

        Args:
            title: Document title
            content: Document content
            source_type: Source type (manual, upload, web)
            source_url: Optional source URL
            use_ai: Whether to use AI for tags/summary generation (default: True)
        """

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

        # Generate AI tags and summary if enabled
        if use_ai:
            try:
                ai_result = self.ai_service.generate_tags_and_summary(
                    title=document.title,
                    content=document.content
                )
                document.tags = ai_result['tags']
                document.summary = ai_result['summary']
            except Exception as e:
                print(f"Warning: AI generation failed: {e}")
                # Continue without AI-generated content
                document.tags = []
                document.summary = None

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

    def search_documents(self, query: str) -> List[Document]:
        """Search documents by title"""
        if not query or len(query.strip()) == 0:
            return []

        return self.repository.search_by_title(query.strip())

    def regenerate_ai_content(self, document_id: int) -> Optional[Document]:
        """Regenerate AI tags and summary for existing document"""
        document = self.repository.get_by_id(document_id)

        if not document:
            return None

        try:
            ai_result = self.ai_service.generate_tags_and_summary(
                title=document.title,
                content=document.content
            )
            document.tags = ai_result['tags']
            document.summary = ai_result['summary']

            return self.repository.update(document)
        except Exception as e:
            print(f"AI regeneration failed: {e}")
            return document