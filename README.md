# RAG-based Question Answering Application

A scalable Retrieval-Augmented Generation (RAG) application that enables document ingestion, embedding generation, and AI-powered question answering based on your uploaded documents.

## Features

- **Document Management**: Upload, list, and manage documents with automatic embedding generation
- **User Authentication**: Register and login with JWT-based authentication
- **Document Selection**: Choose which documents to include in the RAG context
- **Smart Q&A**: Ask questions and get answers based on your selected documents
- **Q&A History**: Track and review previous questions and answers
- **Embeddings-based Retrieval**: Efficiently find the most relevant document sections for answering questions

```
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── qa.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   └── qa_service.py
│   └── main.py
├── requirements.txt
└── .env
```

## Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: SQLite (built-in, no setup required) or PostgreSQL (optional)
- **Embeddings**: Sentence Transformers for document and query embeddings
- **RAG Components**: 
  - LangChain for orchestration
  - Ollama for local LLM inference
  - Sentence Transformers for semantic search
- **Security**: JWT authentication, password hashing with bcrypt

## Getting Started

### Prerequisites

- Python 3.9+
- Pip package manager

### Installation

1. Clone the repository (or download the code)

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. The API will be available at `http://127.0.0.1:8000`
   - Swagger UI documentation: `http://127.0.0.1:8000/docs`
   - ReDoc documentation: `http://127.0.0.1:8000/redoc`

### Configuration

The application is configured through the `.env` file:

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For PostgreSQL configuration:
```
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
```

## API Endpoints

### Authentication

- **POST** `/api/auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```

- **POST** `/api/auth/token` - Login and get access token
  ```json
  {
    "username": "user@example.com",
    "password": "yourpassword"
  }
  ```

### Documents

- **POST** `/api/documents/upload` - Upload a new document
  ```json
  {
    "title": "Document Title",
    "content": "Document content goes here..."
  }
  ```

- **GET** `/api/documents` - List all documents

- **DELETE** `/api/documents/{document_id}` - Delete a document

- **PUT** `/api/documents/{document_id}/select` - Select/deselect a document for Q&A
  ```json
  {
    "is_selected": true
  }
  ```

### Q&A

- **POST** `/api/qa/ask` - Ask a question
  ```json
  {
    "text": "Your question here?",
    "document_id": null  // Optional, if null uses all selected documents
  }
  ```

- **GET** `/api/qa/history` - Get Q&A history

## How It Works

1. **Document Ingestion**: 
   - Documents are uploaded and stored in the database
   - Embeddings are automatically generated using Sentence Transformers

2. **Question Answering**:
   - User submits a question
   - The question is embedded and compared against document embeddings
   - The most relevant document sections are retrieved
   - An LLM uses the retrieved context to generate an answer

## Architecture

The application follows a modular structure:

- **app/api/**: API endpoints and routing
- **app/core/**: Core functionality including configuration and security
- **app/db/**: Database models and connection handling
- **app/services/**: Business logic including embeddings and Q&A

## Advanced Configuration

### Using External LLMs

By default, the application uses Ollama for local LLM inference. To use external APIs like OpenAI:

1. Update the `qa_service.py` file to use a different LLM provider
2. Add the corresponding API keys to your `.env` file

### Database Migration

To switch from SQLite to PostgreSQL:

1. Install PostgreSQL and create a database
2. Update the `DATABASE_URL` in your `.env` file
3. Restart the application

## Troubleshooting

- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Database errors**: Check that your database URL is correct in the `.env` file
- **405 Method Not Allowed**: Ensure you're using the correct HTTP method (GET/POST/etc.)
- **Authentication errors**: Make sure to include the JWT token in the header: `Authorization: Bearer <token>`

## License

This project is available under the MIT License.