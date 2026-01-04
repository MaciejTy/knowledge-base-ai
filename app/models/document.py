from datetime import datetime
from app import db

class Document(db.Model):
    """Model representing a document in the knowledge base"""

    __tablename__ = 'documents'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    #Basic info
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)

    # Metadata
    source_type = db.Column(db.String(50), nullable=False)  # 'upload', 'web', 'manual'
    source_url = db.Column(db.String(500), nullable=True)
    file_path = db.Column(db.String(500), nullable=True)

    # AI-generated fields
    tags = db.Column(db.JSON, default=list)  # tag list as JSON
    embedding = db.Column(db.JSON, nullable=True)  # Vector embedding dla similarity search

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model to dictionary (for API responses)"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'source_type': self.source_type,
            'source_url': self.source_url,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Document {self.id}: {self.title}>'