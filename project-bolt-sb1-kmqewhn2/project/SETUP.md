# ResearchHub AI - Quick Setup Guide

This guide will help you get ResearchHub AI up and running quickly.

## Prerequisites

1. **Node.js 18+** - [Download here](https://nodejs.org/)
2. **Python 3.9+** - [Download here](https://www.python.org/)
3. **Supabase Account** - [Sign up here](https://supabase.com/)
4. **Groq API Key** - [Get key here](https://console.groq.com/)

## Step-by-Step Setup

### 1. Database Setup (Supabase)

1. Create a new Supabase project at https://supabase.com/dashboard
2. Go to **Project Settings** > **Database**
3. Copy your **Connection String** (Direct Connection, not the Session Pooler)
4. The database schema is already created via migrations

### 2. Get API Keys

#### Groq API Key
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you'll need it for backend setup)

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=your_supabase_connection_string_here
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
EOF

# Edit .env file and replace the placeholder values:
# - DATABASE_URL: Your Supabase connection string
# - GROQ_API_KEY: Your Groq API key

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be running at http://localhost:8000

### 4. Frontend Setup

Open a new terminal:

```bash
# Navigate to project root
cd /path/to/researchhub-ai

# Install Node dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start the development server
npm run dev
```

The frontend will be running at http://localhost:5173

## Verification

1. Open http://localhost:5173 in your browser
2. You should see the ResearchHub AI login page
3. Create a new account
4. Try creating a workspace
5. Search for papers from arXiv
6. Import papers and chat with the AI

## Common Issues

### Backend Issues

**Issue**: `ModuleNotFoundError`
**Solution**: Make sure you installed all dependencies: `pip install -r requirements.txt`

**Issue**: Database connection error
**Solution**: Check your DATABASE_URL in backend/.env file

**Issue**: Groq API error
**Solution**: Verify your GROQ_API_KEY is correct in backend/.env file

### Frontend Issues

**Issue**: Cannot connect to backend
**Solution**: Make sure backend is running on port 8000 and check VITE_API_URL in .env

**Issue**: Build errors
**Solution**: Delete node_modules and package-lock.json, then run `npm install` again

## Environment Variables Summary

### Backend (.env in backend/)
```
DATABASE_URL=postgresql://user:pass@host:port/database
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
JWT_SECRET_KEY=random_secure_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (.env in root/)
```
VITE_API_URL=http://localhost:8000
```

## Next Steps

1. Read the main [README.md](README.md) for detailed documentation
2. Check out the API documentation at http://localhost:8000/docs
3. Explore the features:
   - Create multiple workspaces
   - Search and import papers
   - Chat with AI about your research
   - Upload PDF papers

## Production Deployment

For production deployment:

1. Set up a production database (Supabase production tier)
2. Deploy backend to a hosting service (Heroku, Railway, etc.)
3. Deploy frontend to Vercel, Netlify, or similar
4. Update environment variables with production URLs
5. Enable HTTPS for secure communication

## Support

If you encounter any issues:
1. Check the logs in the terminal
2. Review the API documentation at http://localhost:8000/docs
3. Open an issue on the GitHub repository

Happy researching!
