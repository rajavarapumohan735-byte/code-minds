# ResearchHub AI - Complete Project Structure

```
researchhub-ai/
│
├── frontend/                                 # React Frontend Application
│   ├── public/
│   │   └── vite.svg
│   │
│   ├── src/
│   │   ├── components/                      # Reusable React Components
│   │   │   ├── ChatInterface.tsx           # AI chat component with messages
│   │   │   └── PaperSearch.tsx             # Modal for searching papers
│   │   │
│   │   ├── contexts/                        # React Context Providers
│   │   │   └── AuthContext.tsx             # Authentication state management
│   │   │
│   │   ├── pages/                           # Main Application Pages
│   │   │   ├── Login.tsx                   # Login & Register page
│   │   │   ├── Dashboard.tsx               # Workspace list dashboard
│   │   │   └── Workspace.tsx               # Individual workspace view
│   │   │
│   │   ├── services/                        # API Service Layer
│   │   │   └── api.ts                      # All API calls to backend
│   │   │
│   │   ├── App.tsx                          # Main app with routing
│   │   ├── main.tsx                         # React entry point
│   │   ├── index.css                        # Tailwind CSS imports
│   │   └── vite-env.d.ts                   # Vite TypeScript definitions
│   │
│   ├── .env                                 # Frontend environment variables
│   ├── .env.example                         # Environment template
│   ├── index.html                           # HTML entry point
│   ├── package.json                         # Node dependencies
│   ├── tailwind.config.js                   # Tailwind configuration
│   ├── tsconfig.json                        # TypeScript configuration
│   ├── tsconfig.app.json                    # App TypeScript config
│   ├── tsconfig.node.json                   # Node TypeScript config
│   ├── vite.config.ts                       # Vite build configuration
│   └── eslint.config.js                     # ESLint configuration
│
├── backend/                                  # FastAPI Backend Application
│   ├── routers/                             # API Route Handlers
│   │   ├── auth.py                         # Registration & Login endpoints
│   │   ├── workspaces.py                   # Workspace CRUD operations
│   │   ├── papers.py                       # Paper search & management
│   │   └── chat.py                         # AI chat & conversations
│   │
│   ├── models/                              # Data Models
│   │   └── schemas.py                      # Pydantic request/response models
│   │
│   ├── utils/                               # Utility Functions
│   │   ├── auth.py                         # JWT & password hashing
│   │   ├── ai.py                           # Groq API & embeddings
│   │   └── pdf_parser.py                  # PDF text extraction
│   │
│   ├── main.py                              # FastAPI application entry
│   ├── config.py                            # Configuration management
│   ├── database.py                          # Database connection setup
│   ├── requirements.txt                     # Python dependencies
│   ├── .env                                # Backend environment variables
│   ├── .env.example                        # Environment template
│   ├── .gitignore                          # Git ignore patterns
│   └── README.md                           # Backend documentation
│
├── docs/                                    # Documentation Files
│   ├── README.md                           # Main project documentation
│   ├── SETUP.md                            # Detailed setup instructions
│   ├── QUICKSTART.md                       # 5-minute quick start guide
│   ├── FEATURES.md                         # Feature documentation
│   ├── ARCHITECTURE.md                     # System architecture details
│   └── PROJECT_STRUCTURE.md                # This file
│
├── scripts/
│   └── start-dev.sh                        # Development startup script
│
└── .gitignore                              # Root git ignore

```

## File Descriptions

### Frontend Core Files

**App.tsx**
- Main application component
- Routing setup (React Router)
- Authentication guards (PrivateRoute, PublicRoute)
- Auth provider wrapper

**main.tsx**
- React application entry point
- Renders App component
- StrictMode wrapper

**index.css**
- Tailwind CSS imports
- Global styles

### Frontend Pages

**Login.tsx**
- Combined login/register page
- Toggle between modes
- Form validation
- Error handling

**Dashboard.tsx**
- Workspace list view
- Create workspace modal
- Delete workspace functionality
- Navigate to workspaces

**Workspace.tsx**
- Individual workspace view
- Tab interface (Papers/Chat)
- Paper management
- Chat integration

### Frontend Components

**ChatInterface.tsx**
- AI chat component
- Conversation list sidebar
- Message display
- Send message form
- Real-time updates

**PaperSearch.tsx**
- Full-screen search modal
- arXiv API integration
- Search results display
- Import functionality

### Frontend Services

**api.ts**
- Centralized API calls
- Authentication handling
- Error handling
- Type-safe requests

### Frontend Contexts

**AuthContext.tsx**
- Global auth state
- Login/logout functions
- User data management
- Token storage

### Backend Routes

**auth.py**
- POST /auth/register - User registration
- POST /auth/login - User authentication
- Password hashing with bcrypt
- JWT token generation

**workspaces.py**
- POST /workspaces - Create workspace
- GET /workspaces - List user workspaces
- GET /workspaces/{id} - Get workspace details
- PUT /workspaces/{id} - Update workspace
- DELETE /workspaces/{id} - Delete workspace

**papers.py**
- POST /papers/search - Search arXiv papers
- POST /papers/import - Import paper to workspace
- GET /papers/workspace/{id} - List workspace papers
- POST /papers/upload - Upload PDF paper
- DELETE /papers/workspace/{wid}/paper/{pid} - Remove paper

**chat.py**
- POST /chat/conversations - Create conversation
- GET /chat/conversations/workspace/{id} - List conversations
- GET /chat/conversations/{id}/messages - Get messages
- POST /chat - Send message & get AI response
- DELETE /chat/conversations/{id} - Delete conversation

### Backend Utilities

**auth.py**
- Password hashing (bcrypt)
- Password verification
- JWT token creation
- Token decoding
- Current user extraction

**ai.py**
- Groq API integration
- Llama 3.3 70B model
- Embedding generation (sentence-transformers)
- Context building from papers
- Prompt engineering

**pdf_parser.py**
- PDF text extraction
- PyPDF2 integration
- Error handling
- URL and file support

### Backend Core

**main.py**
- FastAPI application
- CORS middleware
- Router registration
- Health check endpoint

**config.py**
- Environment variable management
- Settings validation
- Pydantic settings

**database.py**
- Database connection
- SQLAlchemy setup
- Query execution helpers

**schemas.py**
- Request models
- Response models
- Validation rules

## Database Schema

```
users
├── id (uuid, PK)
├── email (unique)
├── password_hash
├── full_name
├── created_at
└── updated_at

workspaces
├── id (uuid, PK)
├── user_id (FK → users)
├── name
├── description
├── created_at
└── updated_at

papers
├── id (uuid, PK)
├── title
├── authors (array)
├── abstract
├── publication_date
├── pdf_url
├── pdf_text
├── arxiv_id
├── doi
├── embedding (vector)
└── created_at

workspace_papers
├── id (uuid, PK)
├── workspace_id (FK → workspaces)
├── paper_id (FK → papers)
└── added_at

conversations
├── id (uuid, PK)
├── workspace_id (FK → workspaces)
├── title
├── created_at
└── updated_at

messages
├── id (uuid, PK)
├── conversation_id (FK → conversations)
├── role (user/assistant)
├── content
└── created_at
```

## Key Dependencies

### Frontend
- react: ^18.3.1
- react-router-dom: ^6.x
- tailwindcss: ^3.4.1
- lucide-react: ^0.344.0
- vite: ^5.4.2

### Backend
- fastapi: 0.109.0
- uvicorn: 0.27.0
- sqlalchemy: 2.0.25
- groq: 0.4.2
- sentence-transformers: 2.3.1
- python-jose: 3.3.0
- passlib: 1.7.4
- PyPDF2: 3.0.1

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### Backend (backend/.env)
```
DATABASE_URL=postgresql://...
GROQ_API_KEY=gsk_...
JWT_SECRET_KEY=random_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

## Build & Run Commands

### Frontend
```bash
npm install          # Install dependencies
npm run dev         # Development server
npm run build       # Production build
npm run preview     # Preview production build
npm run typecheck   # Type checking
npm run lint        # Linting
```

### Backend
```bash
pip install -r requirements.txt    # Install dependencies
uvicorn main:app --reload         # Development server
python -m pytest                   # Run tests
```

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Features

1. **Authentication**: JWT tokens with bcrypt password hashing
2. **Authorization**: Row Level Security (RLS) on all database tables
3. **CORS**: Configured for frontend-backend communication
4. **Input Validation**: Pydantic models for request validation
5. **SQL Injection Prevention**: Parameterized queries

## Performance Features

1. **Database Indexing**: On foreign keys, vectors, and timestamps
2. **Vector Search**: pgvector with IVFFlat index
3. **Code Splitting**: Vite automatic code splitting
4. **Lazy Loading**: React components loaded on demand
5. **Optimized Bundles**: Production build optimization

## Testing Strategy

### Frontend Testing
- Component testing
- Integration testing
- E2E testing with Playwright

### Backend Testing
- Unit tests with pytest
- API endpoint testing
- Database testing
- Integration testing

## Deployment Checklist

- [ ] Set production environment variables
- [ ] Configure production database
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS for production domain
- [ ] Build frontend for production
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Security audit
- [ ] Performance optimization

## Maintenance

### Regular Tasks
1. Update dependencies monthly
2. Review security advisories
3. Database backups verification
4. Log monitoring
5. Performance metrics review

### Monitoring
- API response times
- Database query performance
- Error rates
- User activity
- Resource usage

