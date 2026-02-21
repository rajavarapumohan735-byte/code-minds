from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WorkspaceResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

class PaperCreate(BaseModel):
    title: str
    authors: List[str] = []
    abstract: str = ""
    publication_date: Optional[date] = None
    pdf_url: Optional[str] = None
    arxiv_id: Optional[str] = None
    doi: Optional[str] = None

class PaperResponse(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    publication_date: Optional[date]
    pdf_url: Optional[str]
    arxiv_id: Optional[str]
    doi: Optional[str]
    created_at: datetime

class PaperImport(BaseModel):
    workspace_id: str
    paper_id: str

class SearchQuery(BaseModel):
    query: str
    limit: int = 10

class ConversationCreate(BaseModel):
    workspace_id: str
    title: Optional[str] = "New Conversation"

class ConversationResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(BaseModel):
    conversation_id: str
    content: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime

class ChatRequest(BaseModel):
    workspace_id: str
    conversation_id: str
    message: str

class ChatResponse(BaseModel):
    message: MessageResponse
    response: MessageResponse
