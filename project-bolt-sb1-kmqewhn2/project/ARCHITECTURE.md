# ResearchHub AI - System Architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                   React + TypeScript                         │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Pages      │  │  Components  │  │   Services   │     │
│  │              │  │              │  │              │     │
│  │  - Login     │  │  - Chat      │  │  - API       │     │
│  │  - Dashboard │  │  - Search    │  │  - Auth      │     │
│  │  - Workspace │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │           React Router + Auth Context            │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend API                             │
│                       FastAPI                                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routers    │  │    Utils     │  │    Models    │     │
│  │              │  │              │  │              │     │
│  │  - Auth      │  │  - JWT       │  │  - Schemas   │     │
│  │  - Papers    │  │  - AI        │  │  - Requests  │     │
│  │  - Workspaces│  │  - PDF       │  │  - Responses │     │
│  │  - Chat      │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         │ PostgreSQL         │ Groq API          │ arXiv API
         ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
│   Supabase DB    │  │  Llama 3.3   │  │    arXiv     │
│                  │  │   70B Model  │  │   Database   │
│  - Users         │  │              │  │              │
│  - Workspaces    │  │  Temperature │  │  Paper       │
│  - Papers        │  │    0.3       │  │  Metadata    │
│  - Conversations │  │  Max 2000    │  │              │
│  - Messages      │  │   tokens     │  │              │
│  - Embeddings    │  │              │  │              │
└──────────────────┘  └──────────────┘  └──────────────┘
```

## Technology Stack

### Frontend Layer

**Framework**: React 18.3.1
- Component-based architecture
- Hooks for state management
- TypeScript for type safety

**Styling**: Tailwind CSS 3.4.1
- Utility-first CSS framework
- Responsive design system
- Custom color palette

**Routing**: React Router v6
- Client-side routing
- Protected routes
- Navigation guards

**State Management**:
- React Context API for auth
- Local component state
- localStorage for persistence

**Build Tool**: Vite 5.4.2
- Fast development server
- Optimized production builds
- Hot module replacement

### Backend Layer

**Framework**: FastAPI 0.109.0
- Async Python web framework
- Automatic API documentation
- Type validation with Pydantic

**Database**: PostgreSQL (Supabase)
- SQLAlchemy ORM
- Raw SQL for complex queries
- Connection pooling

**Authentication**: JWT
- python-jose for tokens
- passlib with bcrypt
- Bearer token auth

**AI Integration**: Groq API
- Llama 3.3 70B model
- Context-aware responses
- Temperature 0.3

**Vector Search**:
- sentence-transformers
- all-MiniLM-L6-v2 model
- pgvector extension

**PDF Processing**: PyPDF2
- Text extraction
- Multi-page support
- Error handling

### Database Layer

**Provider**: Supabase
- Managed PostgreSQL
- Real-time subscriptions
- Built-in auth (not used)
- Row Level Security

**Extensions**:
- pgvector for embeddings
- UUID support
- Full-text search

**Tables**:
1. users - User accounts
2. workspaces - Research workspaces
3. papers - Research papers
4. workspace_papers - Many-to-many
5. conversations - Chat sessions
6. messages - Chat messages

## Data Flow

### Authentication Flow

```
1. User Registration/Login
   ↓
2. Frontend sends credentials
   ↓
3. Backend validates
   ↓
4. Password hashing (bcrypt)
   ↓
5. JWT token generation
   ↓
6. Token sent to frontend
   ↓
7. Token stored in localStorage
   ↓
8. Token included in all requests
```

### Paper Search Flow

```
1. User enters search query
   ↓
2. Frontend sends to backend
   ↓
3. Backend queries arXiv API
   ↓
4. Parse XML response
   ↓
5. Generate embeddings
   ↓
6. Store in database
   ↓
7. Return results to frontend
   ↓
8. Display in search modal
```

### AI Chat Flow

```
1. User sends message
   ↓
2. Frontend sends to backend
   ↓
3. Backend retrieves workspace papers
   ↓
4. Build context from papers
   ↓
5. Retrieve conversation history
   ↓
6. Create prompt with context
   ↓
7. Send to Groq API
   ↓
8. Receive AI response
   ↓
9. Store messages in database
   ↓
10. Return to frontend
    ↓
11. Display in chat interface
```

## Security Architecture

### Authentication Security

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ Email + Password
       ▼
┌─────────────┐
│   Backend   │
│             │
│  1. Hash    │
│  2. Compare │
│  3. Generate│
│     JWT     │
└──────┬──────┘
       │ JWT Token
       ▼
┌─────────────┐
│   Client    │
│  localStorage│
└──────┬──────┘
       │ Bearer Token
       ▼
┌─────────────┐
│  Protected  │
│  Resources  │
└─────────────┘
```

### Database Security

**Row Level Security (RLS)**:
```sql
-- Example: Users can only see their own workspaces
CREATE POLICY "Users can view own workspaces"
  ON workspaces FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());
```

**Benefits**:
- Automatic enforcement
- Database-level security
- No code bypasses
- Query-level filtering

## API Architecture

### Endpoint Organization

```
/api
├── /auth
│   ├── POST /register
│   └── POST /login
├── /workspaces
│   ├── GET    /
│   ├── POST   /
│   ├── GET    /{id}
│   ├── PUT    /{id}
│   └── DELETE /{id}
├── /papers
│   ├── POST   /search
│   ├── POST   /import
│   ├── GET    /workspace/{id}
│   ├── POST   /upload
│   └── DELETE /workspace/{workspace_id}/paper/{paper_id}
└── /chat
    ├── POST   /conversations
    ├── GET    /conversations/workspace/{id}
    ├── GET    /conversations/{id}/messages
    ├── POST   /
    └── DELETE /conversations/{id}
```

### Request/Response Format

**Request**:
```json
{
  "field": "value",
  "nested": {
    "key": "value"
  }
}
```

**Success Response**:
```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```

## Component Architecture

### Frontend Components

```
App.tsx (Root)
├── AuthProvider (Context)
├── BrowserRouter
└── Routes
    ├── PublicRoute
    │   └── Login
    └── PrivateRoute
        ├── Dashboard
        │   └── WorkspaceCard[]
        └── Workspace
            ├── PaperList
            │   └── Paper[]
            └── ChatInterface
                ├── ConversationList
                │   └── Conversation[]
                └── MessageList
                    └── Message[]
```

### Backend Structure

```
backend/
├── main.py (FastAPI app)
├── config.py (Settings)
├── database.py (DB connection)
├── models/
│   └── schemas.py (Pydantic models)
├── routers/
│   ├── auth.py
│   ├── workspaces.py
│   ├── papers.py
│   └── chat.py
└── utils/
    ├── auth.py (JWT, passwords)
    ├── ai.py (Groq, embeddings)
    └── pdf_parser.py (PDF processing)
```

## Scalability Considerations

### Current Architecture
- Single backend server
- Single database instance
- Direct API calls

### Potential Scaling

**Horizontal Scaling**:
- Multiple backend instances
- Load balancer
- Session management

**Database Scaling**:
- Read replicas
- Connection pooling
- Query optimization

**Caching**:
- Redis for sessions
- Cache API responses
- CDN for static assets

**Background Jobs**:
- Celery for PDF processing
- Queue for embeddings
- Async task processing

## Deployment Architecture

### Development
```
localhost:5173 (Frontend) → localhost:8000 (Backend) → Supabase
```

### Production
```
CDN → Frontend (Vercel/Netlify)
         ↓
API Gateway → Backend (Railway/Heroku)
                ↓
         Supabase (Production)
```

## Monitoring & Logging

### Backend Logging
- Request/response logging
- Error tracking
- Performance metrics
- API usage statistics

### Frontend Monitoring
- Error boundaries
- Performance tracking
- User analytics
- Console error logging

## Backup & Recovery

### Database Backups
- Automatic Supabase backups
- Point-in-time recovery
- Export functionality

### Data Recovery
- RLS prevents data loss
- Cascade deletions configured
- Soft delete options

## Performance Optimization

### Frontend
- Code splitting
- Lazy loading
- Bundle optimization
- Asset compression

### Backend
- Connection pooling
- Query optimization
- Response caching
- Index optimization

### Database
- Vector indexes
- Foreign key indexes
- Query planning
- EXPLAIN analysis

## Conclusion

ResearchHub AI uses a modern, scalable architecture that separates concerns, ensures security, and provides excellent performance. The system is designed to be maintainable, extensible, and production-ready.
