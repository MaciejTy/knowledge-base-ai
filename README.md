# Knowledge Base AI

AI-powered personal knowledge base system built with Flask, PostgreSQL, and Claude API.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete documents
- **AI Integration**: Auto-generate tags and summaries using Claude API
- **Smart Search**: Search documents by title
- **RESTful API**: Clean REST endpoints with proper HTTP status codes
- **Layered Architecture**: Separation of concerns with Repository and Service patterns
- **Database Migrations**: Managed with Flask-Migrate (Alembic)

## 🛠️ Tech Stack

- **Backend**: Flask 3.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 3.1
- **Migrations**: Alembic (Flask-Migrate)
- **AI**: Anthropic Claude API
- **Language**: Python 3.12

## 📁 Project Structure
```
knowledge-base-ai/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration settings
│   ├── models/
│   │   └── document.py          # Document model (database schema)
│   ├── repositories/
│   │   └── document_repository.py  # Data access layer
│   ├── services/
│   │   └── document_service.py  # Business logic layer
│   └── api/routes/
│       └── documents.py         # REST API endpoints
├── migrations/                   # Database migrations
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables (not in repo)
```

## 🏗️ Architecture

The project follows a **layered architecture** pattern:
```
HTTP Request → Routes → Services → Repositories → Models → Database
```

- **Routes**: Handle HTTP requests/responses
- **Services**: Business logic and validation
- **Repositories**: Database operations
- **Models**: Database schema definitions

## 📦 Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/MaciejTy/knowledge-base-ai.git
cd knowledge-base-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL database**
```bash
# Create database
createdb knowledge_base

# Or using psql
psql -U postgres
CREATE DATABASE knowledge_base;
\q
```

5. **Configure environment variables**

Create `.env` file:
```bash
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/knowledge_base
ANTHROPIC_API_KEY=your_claude_api_key_here
SECRET_KEY=your-secret-key-here
```

6. **Run database migrations**
```bash
flask db upgrade
```

7. **Start the server**
```bash
python run.py
```

Server will run on `http://127.0.0.1:5000`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:5000/api
```

### Endpoints

#### Create Document
```http
POST /documents
Content-Type: application/json

{
  "title": "Document Title",
  "content": "Document content here...",
  "source_type": "manual"  // optional: "manual", "upload", "web"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Document Title",
  "content": "Document content here...",
  "summary": null,
  "tags": [],
  "source_type": "manual",
  "created_at": "2025-01-04T20:30:00",
  "updated_at": "2025-01-04T20:30:00"
}
```

#### Get All Documents
```http
GET /documents?limit=10&offset=0
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Document Title",
    ...
  }
]
```

#### Get Single Document
```http
GET /documents/{id}
```

**Response:** `200 OK` or `404 Not Found`

#### Update Document
```http
PUT /documents/{id}
Content-Type: application/json

{
  "title": "Updated Title",
  "tags": ["python", "flask"],
  "summary": "Brief summary"
}
```

**Response:** `200 OK` or `404 Not Found`

#### Delete Document
```http
DELETE /documents/{id}
```

**Response:** `200 OK` or `404 Not Found`

#### Search Documents
```http
GET /documents/search?q=python
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Python Programming Guide",
    ...
  }
]
```

## 🧪 Example Usage

### Using cURL
```bash
# Create a document
curl -X POST http://127.0.0.1:5000/api/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Flask Tutorial", "content": "Learn Flask framework..."}'

# Get all documents
curl http://127.0.0.1:5000/api/documents

# Search documents
curl "http://127.0.0.1:5000/api/documents/search?q=flask"

# Update document
curl -X PUT http://127.0.0.1:5000/api/documents/1 \
  -H "Content-Type: application/json" \
  -d '{"tags": ["python", "flask", "backend"]}'

# Delete document
curl -X DELETE http://127.0.0.1:5000/api/documents/1
```

## 🤖 AI Features (Coming Soon)

- Auto-generate tags from document content
- Auto-generate summaries
- Semantic search using embeddings
- Document similarity detection

## 🔧 Development

### Database Migrations
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### Flask Shell
```bash
flask shell

# Now you have access to:
>>> db
>>> Document
```

## 📝 License

This project is for educational purposes.

## 👤 Author

**Maciej Tyszczuk**
- GitHub: [@MaciejTy](https://github.com/MaciejTy)