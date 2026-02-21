# ResearchHub AI

An intelligent research paper management and analysis system powered by agentic AI. ResearchHub AI helps researchers organize, analyze, and extract insights from academic papers using advanced AI technology.

## Features

- **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Research Paper Search**: Search academic papers from arXiv API
- **Paper Management**: Import and organize papers in custom workspaces
- **AI-Powered Chat**: Context-aware AI assistant powered by Groq Llama 3.3 70B
- **Vector Search**: Semantic search using sentence-transformers embeddings
- **Multi-Workspace Support**: Organize papers into different research projects
- **Conversation History**: Persistent chat history for each workspace
- **PDF Processing**: Upload and extract text from PDF papers

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Lucide React for icons
- Vite for build tooling

### Backend
- FastAPI (Python)
- PostgreSQL database (via Supabase)
- SQLAlchemy for database operations
- Groq API with Llama 3.3 70B model
- sentence-transformers for embeddings
- PyPDF2 for PDF parsing
- python-jose for JWT tokens
- passlib for password hashing

### Database
- Supabase PostgreSQL with pgvector extension
- Vector embeddings for semantic search
- Row Level Security (RLS) policies

## Project Structure

```
researchhub-ai/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── routers/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── workspaces.py     # Workspace management
│   │   ├── papers.py         # Paper management
│   │   └── chat.py           # AI chat endpoints
│   └── utils/
│       ├── auth.py           # JWT and password utilities
│       ├── ai.py             # Groq AI integration
│       └── pdf_parser.py     # PDF text extraction
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx  # AI chat component
│   │   └── PaperSearch.tsx    # Paper search modal
│   ├── contexts/
│   │   └── AuthContext.tsx    # Authentication context
│   ├── pages/
│   │   ├── Login.tsx          # Login/Register page
│   │   ├── Dashboard.tsx      # Workspace dashboard
│   │   └── Workspace.tsx      # Workspace detail view
│   ├── services/
│   │   └── api.ts             # API service layer
│   ├── App.tsx                # Main app component
│   └── main.tsx               # React entry point
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Supabase account (for database)
- Groq API key (for AI features)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory:
```bash
DATABASE_URL=your_supabase_postgres_connection_string
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_random_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the project root directory

2. Install Node dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory:
```bash
VITE_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Database Setup

The database schema is automatically set up via Supabase migrations. The schema includes:

- **users**: User accounts with authentication
- **workspaces**: Research workspaces
- **papers**: Research papers with vector embeddings
- **workspace_papers**: Many-to-many relationship
- **conversations**: Chat conversations
- **messages**: Chat messages

All tables have Row Level Security (RLS) enabled to ensure users can only access their own data.

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key API Endpoints

**Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

**Workspaces**
- `POST /workspaces` - Create workspace
- `GET /workspaces` - List user workspaces
- `GET /workspaces/{id}` - Get workspace details
- `PUT /workspaces/{id}` - Update workspace
- `DELETE /workspaces/{id}` - Delete workspace

**Papers**
- `POST /papers/search` - Search papers from arXiv
- `POST /papers/import` - Import paper to workspace
- `GET /papers/workspace/{workspace_id}` - Get workspace papers
- `POST /papers/upload` - Upload PDF paper
- `DELETE /papers/workspace/{workspace_id}/paper/{paper_id}` - Remove paper

**Chat**
- `POST /chat/conversations` - Create conversation
- `GET /chat/conversations/workspace/{workspace_id}` - List conversations
- `GET /chat/conversations/{conversation_id}/messages` - Get messages
- `POST /chat` - Send message and get AI response
- `DELETE /chat/conversations/{conversation_id}` - Delete conversation

## AI Features

### Groq Llama 3.3 70B Integration

The AI chatbot uses Groq's Llama 3.3 70B model with:
- Temperature: 0.3 (for focused, consistent responses)
- Max tokens: 2000
- Context-aware responses based on workspace papers

### Vector Search

Papers are automatically converted to embeddings using sentence-transformers (all-MiniLM-L6-v2 model) and stored in PostgreSQL with pgvector extension for semantic search capabilities.

### AI Capabilities

The AI assistant can:
- Summarize individual research papers
- Compare and contrast multiple papers
- Answer questions about research findings
- Extract key insights and methodologies
- Explain complex concepts
- Provide research recommendations

## Usage Guide

1. **Register/Login**: Create an account or login
2. **Create Workspace**: Set up a workspace for your research project
3. **Search Papers**: Search for papers from arXiv and import them
4. **Upload PDFs**: Upload your own PDF papers
5. **Chat with AI**: Ask questions about your papers, get summaries, and insights
6. **Organize**: Create multiple workspaces for different projects

## Security

- JWT-based authentication with secure token storage
- Bcrypt password hashing
- Row Level Security (RLS) on all database tables
- API authentication required for all protected endpoints
- CORS configured for frontend-backend communication

## Development

### Running Tests

```bash
npm run lint
npm run typecheck
```

### Building for Production

Frontend:
```bash
npm run build
```

Backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues and questions, please open an issue on the GitHub repository.
