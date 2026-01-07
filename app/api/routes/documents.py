from flask import Blueprint, request, jsonify
from app.services import DocumentService

# Blueprint groups related routes together
bp = Blueprint('documents', __name__, url_prefix='/api/documents')

# Initialize service instance
document_service = DocumentService()


@bp.route('', methods=['POST'])
def create_document():
    """
    Create a new document

    POST /api/documents
    Body: {"title": "...", "content": "...", "source_type": "manual"}
    Returns: 201 Created with document JSON
    """
    try:
        # Parse JSON from request body
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400

        # Delegate to service layer (handles business logic)
        document = document_service.create_document(
            title=data['title'],
            content=data['content'],
            source_type=data.get('source_type', 'manual'),
            source_url=data.get('source_url')
        )

        # Return JSON response with 201 Created status
        return jsonify(document.to_dict()), 201

    except ValueError as e:
        # Service validation error (e.g., empty title)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Unexpected error
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('/<int:document_id>', methods=['GET'])
def get_document(document_id):
    """
    Get a document by ID

    GET /api/documents/1
    Returns: 200 OK with document JSON or 404 Not Found
    """
    try:
        document = document_service.get_document(document_id)

        if not document:
            return jsonify({'error': 'Document not found'}), 404

        return jsonify(document.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('', methods=['GET'])
def list_documents():
    """
    List all documents with pagination

    GET /api/documents?limit=10&offset=0
    Returns: 200 OK with array of documents
    """
    try:
        # Extract query parameters from URL
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)

        documents = document_service.list_documents(limit=limit, offset=offset)

        # Convert each document to dictionary
        return jsonify([doc.to_dict() for doc in documents]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('/<int:document_id>', methods=['PUT'])
def update_document(document_id):
    """
    Update a document

    PUT /api/documents/1
    Body: {"title": "New title", "tags": ["python", "flask"]}
    Returns: 200 OK with updated document or 404 Not Found
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Service will only update allowed fields
        document = document_service.update_document(document_id, **data)

        if not document:
            return jsonify({'error': 'Document not found'}), 404

        return jsonify(document.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """
    Delete a document

    DELETE /api/documents/1
    Returns: 200 OK with success message or 404 Not Found
    """
    try:
        success = document_service.delete_document(document_id)

        if not success:
            return jsonify({'error': 'Document not found'}), 404

        return jsonify({'message': 'Document deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('/search', methods=['GET'])
def search_documents():
    """
    Search documents by title

    GET /api/documents/search?q=python
    Returns: 200 OK with array of matching documents
    """
    try:
        query = request.args.get('q', '')

        if not query:
            return jsonify({'error': 'Query parameter q is required'}), 400

        documents = document_service.search_documents(query)

        return jsonify([doc.to_dict() for doc in documents]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@bp.route('/<int:document_id>/regenerate-ai', methods=['POST'])
def regenerate_ai_content(document_id):
    """
    Regenerate AI tags and summary for existing document

    POST /api/documents/1/regenerate-ai
    Returns: 200 OK with updated document or 404 Not Found
    """
    try:
        document = document_service.regenerate_ai_content(document_id)

        if not document:
            return jsonify({'error': 'Document not found'}), 404

        return jsonify(document.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500