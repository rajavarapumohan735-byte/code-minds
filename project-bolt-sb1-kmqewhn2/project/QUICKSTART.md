# ResearchHub AI - Quick Start Guide

Get ResearchHub AI running in 5 minutes!

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.9+ installed
- [ ] Supabase account created
- [ ] Groq API key obtained

## Configuration

### 1. Supabase Setup

The database is already configured! Just update the connection string:

**Location**: `backend/.env`

```env
DATABASE_URL=postgresql://postgres.bmpvdrvfabpmdvevdrxo:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

Replace `[YOUR-PASSWORD]` with your Supabase database password.

### 2. Groq API Key

**Location**: `backend/.env`

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your key at: https://console.groq.com/

## Start the Application

### Option 1: Automatic (Recommended)

```bash
chmod +x start-dev.sh
./start-dev.sh
```

### Option 2: Manual

**Terminal 1 - Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
npm install
npm run dev
```

## Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## First Steps

1. **Register**: Create your account at http://localhost:5173
2. **Create Workspace**: Click "New Workspace"
3. **Search Papers**: Click "Search Papers" and try: "machine learning"
4. **Import Papers**: Click "Import" on any paper
5. **Chat with AI**: Go to "AI Chat" tab and ask: "Summarize the papers"

## Environment Variables Reference

### Backend (`backend/.env`)
```env
DATABASE_URL=your_supabase_connection_string
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (`.env`)
```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version`
- Install dependencies: `pip install -r backend/requirements.txt`
- Verify DATABASE_URL in backend/.env

### Frontend won't start
- Check Node version: `node --version`
- Clear cache: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`

### Can't connect to database
- Verify Supabase password in DATABASE_URL
- Check Supabase project is active
- Test connection from Supabase dashboard

### AI chat not working
- Verify GROQ_API_KEY in backend/.env
- Check Groq API quota at console.groq.com
- Ensure papers are imported in workspace

## Project Structure

```
researchhub-ai/
├── backend/          # FastAPI backend
│   ├── main.py      # Entry point
│   ├── routers/     # API endpoints
│   └── utils/       # AI, auth, PDF
├── src/             # React frontend
│   ├── pages/       # Main pages
│   ├── components/  # Reusable components
│   └── services/    # API calls
└── README.md        # Full documentation
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Get JWT token

### Workspaces
- `GET /workspaces` - List workspaces
- `POST /workspaces` - Create workspace

### Papers
- `POST /papers/search` - Search arXiv
- `POST /papers/import` - Add to workspace
- `GET /papers/workspace/{id}` - List papers

### Chat
- `POST /chat` - Send message to AI
- `GET /chat/conversations/workspace/{id}` - List chats

## Need Help?

1. Check [README.md](README.md) for detailed docs
2. Visit [SETUP.md](SETUP.md) for detailed setup
3. Review [FEATURES.md](FEATURES.md) for all features
4. See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

## What's Next?

- Try different search queries
- Upload your own PDF papers
- Create multiple workspaces
- Ask AI to compare papers
- Organize papers by topic

Enjoy ResearchHub AI!
