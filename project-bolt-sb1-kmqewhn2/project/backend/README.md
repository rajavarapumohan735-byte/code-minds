# ResearchHub AI - Backend

FastAPI backend for ResearchHub AI - an intelligent research paper management and analysis system.

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
DATABASE_URL=your_supabase_postgres_connection_string
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_random_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### 3. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Workspaces
- `POST /workspaces` - Create a new workspace
- `GET /workspaces` - Get all user workspaces
- `GET /workspaces/{workspace_id}` - Get specific workspace
- `PUT /workspaces/{workspace_id}` - Update workspace
- `DELETE /workspaces/{workspace_id}` - Delete workspace

### Papers
- `POST /papers/search` - Search papers from arXiv
- `POST /papers/import` - Import paper to workspace
- `GET /papers/workspace/{workspace_id}` - Get papers in workspace
- `POST /papers/upload` - Upload PDF paper
- `DELETE /papers/workspace/{workspace_id}/paper/{paper_id}` - Remove paper from workspace

### Chat
- `POST /chat/conversations` - Create new conversation
- `GET /chat/conversations/workspace/{workspace_id}` - Get workspace conversations
- `GET /chat/conversations/{conversation_id}/messages` - Get conversation messages
- `POST /chat` - Send message and get AI response
- `DELETE /chat/conversations/{conversation_id}` - Delete conversation

## Features

- JWT-based authentication with bcrypt password hashing
- Integration with arXiv API for paper search
- Vector embeddings using sentence-transformers
- AI-powered chat using Groq Llama 3.3 70B
- PDF parsing and text extraction
- Semantic search capabilities
- Multi-workspace support
- Conversation history management

## Tech Stack

- FastAPI - Web framework
- PostgreSQL - Database (via Supabase)
- SQLAlchemy - ORM
- Groq API - AI chat
- sentence-transformers - Embeddings
- PyPDF2 - PDF parsing
- python-jose - JWT tokens
- passlib - Password hashing
